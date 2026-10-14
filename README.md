# Guitar Shop Website

A handwritten multi-page guitar-store interface prototype built with HTML, CSS and JavaScript.

Chen Jiang’s University of Melbourne computing coursework.

University: University of Melbourne  

## Implementation

Home, shop/search, product, cart, checkout, story and contact pages; desktop/mobile layouts, navigation overlays, and order-summary toggling.

## Technical approach

The original eight HTML pages retain their CSS and small class-toggle JavaScript mechanism. The root entry redirects to the original home page.

Navigation and order-summary controls use the preserved show/hide classes, with keyboard handling and accessibility state layered onto those same controls.

## Run

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this directory and open http://127.0.0.1:8000/. Browser tests: install `requirements-dev.txt` in a venv, ensure local Google Chrome is available, then run `python3 -B -m unittest discover -s tests -v`.

## Checks and results

- Chrome via Playwright: all nine entry/page URLs passed at 1280×900, 768×1024 and 375×812; no page errors, HTTP asset failures, broken images, horizontal overflow or unnamed form controls.
- Two browser test methods passed, including Enter/Space/Escape, hidden-menu focus isolation, order-summary toggling and a missing-element call.
- Final tablet home screenshot visually inspected; screenshots for the full page matrix are retained privately.

## 2026 maintenance

- Extended the existing responsive breakpoint to cover tablet widths, resolving horizontal overflow.
- Added form-control names, keyboard-operable menu/order controls, Escape closing, focus return and inert hidden navigation.
- Guarded missing DOM elements and added an explicit root entry.
- Added browser regressions covering all pages, local assets and three viewports without external requests or form submission.

These changes are 2026 AI-assisted maintenance of the original student implementation.

## Usage notes

- This is a front-end prototype: search, checkout, payment and account persistence have no backend implementation.
- External fonts were blocked during local verification and were not tested online.
- The publishing/history copy in [chenjiang0819.github.io](https://github.com/chenjiang0819/chenjiang0819.github.io) is documented separately and has not received these source-level UI changes.

## Original project notes

# GuitarShop

### Mock-up  
https://xd.adobe.com/view/bb791fe7-c154-4b92-bd2b-53e0fc0dad5d-ee2a/  

### Introduction  
- The purpose of this project is to redesign the website of the Twangcentral.  
- Their old version of the website has zero responsive design. The webpage cannot even be wholly displayed on a smartphone screen. Thus, we need to design a mobile version of the website for them.  
- Furthermore, due to selling high priced products, we need to be very careful to avoid any suspect black patterns.
