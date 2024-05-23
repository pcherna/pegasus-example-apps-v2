# Changelog -- Example Apps for Saas Pegasus, v2

## v2.4 – 23-May-2024

* Fix back button after using htmx paginator.

## v2.3 – 23-May-2024

* Fixed responsive layout of left-nav items
* Pegasus already includes htmx and alpinejs, so we no longer pull in our own versions.
* Verified against Pegasus 2024.5.3.

## v2.2 – 2-Feb-2024

* Fixed HTMX pagination in function-based views. The context was missing `is_paginated`
* Paginator is easier to understand when `on_ends=1` rather than `2`, meaning we always show the page-number of the first and last page, instead of the first two and last two pages.

## v2.1 – 11-Feb-2023

* Added **crud_example3** which contains **PermThing**, that shows off the use of permissions to shape the GUI and capabilities.
* Added **crud_example4** which contains **InputThing**, that shows off enhanced input fields, plus client-side behaviors using AlpineJS.

## v2.0 – 8-Feb-2023

* Initial release
* Based on my earlier <https://github.com/pcherna/pegasus-example-apps>
* Cleaner organization, removed many quirks
* Much better paginator template and code
