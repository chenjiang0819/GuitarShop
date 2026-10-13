"""Local Chrome regressions; external resources and submissions are blocked."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import os,threading,unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp=ROOT/'.build/browser-temp';tmp.mkdir(parents=True,exist_ok=True);os.environ['TMPDIR']=str(tmp)
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/'
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='chrome',headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def context(self,width,height):
        context=self.browser.new_context(viewport={'width':width,'height':height})
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(self.url) else route.abort())
        self.addCleanup(context.close);return context
    def test_every_page_at_three_viewports(self):
        for width,height in [(1280,900),(768,1024),(375,812)]:
            context=self.context(width,height)
            for file in sorted(ROOT.glob('*.html')):
                with self.subTest(page=file.name,width=width):
                    page=context.new_page();errors=[];failures=[]
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.on('response',lambda r:failures.append(r.url) if r.status>=400 else None)
                    page.goto(self.url+file.name,wait_until='networkidle')
                    self.assertFalse(errors);self.assertFalse(failures)
                    self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth-innerWidth'),0)
                    self.assertEqual(page.evaluate('Array.from(document.images).filter(x=>!x.complete||!x.naturalWidth).length'),0)
                    self.assertEqual(page.locator('input:not([aria-label]):not([aria-labelledby]),textarea:not([aria-label]),select:not([aria-label])').count(),0)
                    page.close()
    def test_keyboard_navigation_and_safe_dom(self):
        context=self.context(375,812);page=context.new_page();page.goto(self.url,wait_until='networkidle')
        self.assertTrue(page.url.endswith('/home.html'))
        self.assertFalse(page.evaluate('switchClass("missing-test-element","test-class")'))
        opener=page.get_by_role('button',name='Open navigation');opener.focus();page.keyboard.press('Enter')
        self.assertEqual(page.locator('#floatNav').get_attribute('aria-hidden'),'false')
        page.get_by_role('button',name='Close navigation').press('Space')
        self.assertEqual(page.locator('#floatNav').get_attribute('aria-hidden'),'true')
        self.assertTrue(page.locator('#floatNav').evaluate('(x)=>x.inert'))
        opener.press('Enter');page.keyboard.press('Escape')
        self.assertEqual(page.locator('#floatNav').get_attribute('aria-hidden'),'true')
        opener.press('Tab')
        self.assertFalse(page.evaluate('document.getElementById("floatNav").contains(document.activeElement)'))
        page.goto(self.url+'checkout.html',wait_until='networkidle')
        toggle=page.get_by_role('button',name='Toggle order summary');toggle.press('Enter')
        self.assertTrue(page.locator('#basket').evaluate('x=>x.classList.contains("show")'))
        toggle.press('Space');self.assertFalse(page.locator('#basket').evaluate('x=>x.classList.contains("show")'))
        page.close()
if __name__=='__main__':unittest.main()
