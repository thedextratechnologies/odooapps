.. image:: https://img.shields.io/badge/license-LGPL--3-green.svg
    :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

Company Account Number & Credit Control
=======================================

Automatically assigns a unique account number to credit-controlled companies and
blocks Sales Order confirmation when a customer's credit limit would be exceeded.

Configuration
=============

* Enable the standard **Partner Limit** option on a company (Accounting tab) and
  set the credit limit amount. The account number is generated automatically.
* No additional configuration is needed.
* The number format (prefix ``P``, 5 digits) can be changed under
  *Settings > Technical > Sequences* (sequence code ``res.partner.account``).

Features
========

* Unique company account numbers (P00001, P00002, ...)
* Numbers assigned only to companies with Partner Limit enabled
* Existing eligible companies numbered automatically on installation
* Database-level uniqueness guarantee
* Strict credit-limit validation on Sales Order confirmation
* Credit exposure = Total Receivable + Confirmed Orders Not Yet Invoiced +
  Quotation(s) Being Confirmed
* Batch confirmation checked as a group (no limit bypass)
* Multi-company and multi-currency support
* Clear error message showing limit, receivable, pending orders and total exposure
* Standard behaviour unchanged when Partner Limit is disabled

Compatibility
=============

* Odoo 19.0 (Enterprise and Community)
* Depends on ``sale_management`` and ``account``

License
=======

GNU Lesser General Public License, Version 3 (LGPL v3).

https://www.gnu.org/licenses/lgpl-3.0-standalone.html

Company
=======

* `Dextra Technologies <https://www.dextratechnologies.com/>`__

Credits
=======

* Developer: Dharshini Vijayapandiyan
  Contact: thedextratechnologies@gmail.com

Contacts
========

* Mail Contact : thedextratechnologies@gmail.com
* Website : https://www.dextratechnologies.com/
* Phone : +91 7397261418

Bug Tracker
===========

In case of any issue or bug report, please contact the support team via email.

Maintainer
==========

.. image:: https://www.dextratechnologies.com/theme/imgs/logo.webp
   :target: https://www.dextratechnologies.com/

This module is maintained by Dextra Technologies.

For support and more information, please visit
`Our Website <https://www.dextratechnologies.com/>`__

Further Information
===================

HTML Description: `<static/description/index.html>`__