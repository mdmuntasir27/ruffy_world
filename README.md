# Ruffy World 🐾

**Ruffy World** is a modern, full-stack pet adoption, veterinary care directory, and pet accessories e-commerce platform built with Python, Django, and Django REST Framework. The application connects loving families with rescue pets, allows community members to post pets for rehoming, facilitates 24/7 veterinary consultations across 8-hour shifts with automatic real-time shift detection, and features an integrated single-vendor pet accessory store with real-time inventory management, checkout (Cash on Delivery or Online Dummy Payment), downloadable digital PDF receipts, a custom administration panel (`/admin-panel/`), phone and email formatting verification, and the calming **"Deep Breath"** color palette with light and dark mode consistency.

---

## Accessing the Custom Admin Panel (`/admin-panel/`)

Ruffy World includes a dedicated, feature-packed custom administrative portal at `/admin-panel/` built with a modern UI to replace the default Django admin panel.

### Administrative Credentials
- **Access URL**: `http://127.0.0.1:8000/admin-panel/`
- **Username**: `admin`
- **Password**: `admin123`

*(Note: Navigating to `/admin/` will automatically redirect you to `/admin-panel/`.)*

### Features Included in the Custom Admin Panel
1. **Interactive KPI Dashboard**: Overview metrics displaying total pets, available pets, pending adoption applications, store inventory count, out-of-stock alerts, total orders, completed store revenue, active on-duty vets, and registered community members.
2. **Pets Management (`/admin-panel/pets/`)**: Full CRUD operations for store pets. Create, view, edit descriptions, adjust adoption fees, configure price types (Fixed / Negotiable), and set adoption status.
3. **Adoption Applications (`/admin-panel/adoptions/`)**: Review detailed applicant questionnaires, past pet experience, contact details, and update application status (`Pending`, `Approved`, `Rejected`) with an option to automatically mark the target pet as `Adopted`.
4. **Store Products & Inventory (`/admin-panel/products/`)**: Add, edit, or delete pet accessories across 10 categories. Manage quantities in real time; setting quantity to `0` automatically flags the item as **Out of Stock**.
5. **Customer Orders (`/admin-panel/orders/`)**: Track customer orders, view ordered item breakdowns, update payment statuses (`Pending`, `Paid`), change shipping progress (`Pending`, `Confirmed`, `Processing`, `Shipped`, `Delivered`, `Cancelled`), and open digital PDF receipts.
6. **Veterinarians Directory (`/admin-panel/vets/`)**: Add, edit, and manage 24/7 veterinarians, schedule them across Morning, Mid, or Night shifts, and toggle active availability.
7. **Community Posts & Inquiries (`/admin-panel/community/`)**: Review and moderate member-submitted adoption posts and user-to-user inquiries.
8. **User Accounts Management (`/admin-panel/users/`)**: Manage accounts, toggle staff privileges, or activate/deactivate accounts. **Security Policy**: In compliance with security requirements, administrators cannot view or reset user passwords; password recovery is strictly performed by users themselves via the self-service verification flow.

---

## Project Structure

```text
ruffy_world/
├── accounts/                     # User authentication, profiles, & password recovery
│   ├── migrations/               # Database migrations for accounts
│   │   ├── 0001_initial.py       # Initial UserProfile model migration
│   │   └── __init__.py           # Accounts migrations package marker
│   ├── admin.py                  # Custom UserAdmin with password change disabled
│   ├── apps.py                   # Accounts app configuration
│   ├── forms.py                  # Register, ProfileUpdate, ForgotPassword forms
│   ├── models.py                 # UserProfile model with phone, location, and bio
│   ├── signals.py                # Post-save signals for automatic profile generation
│   ├── tests.py                  # Unit tests for accounts, validation, and password reset
│   ├── urls.py                   # Routes for register, login, logout, profile, forgot-password
│   ├── validators.py             # Phone (01XXXXXXXXX), email, & password strength validators
│   ├── views.py                  # Authentication, profile, & direct password reset views
│   └── __init__.py               # Accounts app package marker
├── adoptions/                    # Foundation pet adoption requests and dashboard
│   ├── migrations/               # Database migrations for adoptions
│   │   ├── 0001_initial.py       # Initial AdoptionRequest model migration
│   │   └── __init__.py           # Adoptions migrations package marker
│   ├── admin.py                  # Admin management for foundation adoption requests
│   ├── api_urls.py               # REST API endpoints for adoption requests
│   ├── api_views.py              # REST API ViewSets for adoption applications
│   ├── apps.py                   # Adoptions app configuration
│   ├── forms.py                  # Foundation pet adoption application form
│   ├── models.py                 # AdoptionRequest model with status tracking
│   ├── serializers.py            # DRF serializers for adoption requests
│   ├── tests.py                  # Unit tests for adoption application logic
│   ├── urls.py                   # Adoption application and dashboard URLs
│   ├── views.py                  # Apply for adoption and unified requests view
│   └── __init__.py               # Adoptions app package marker
├── community/                    # Community rehoming board and user-to-user inquiries
│   ├── migrations/               # Database migrations for community
│   │   ├── 0001_initial.py       # Initial AdoptionPost and Inquiry models
│   │   ├── 0002_alter_adoptionpost_age.py # Migration: age as text CharField
│   │   ├── 0003_alter_adoptioninquiry_status.py # Migration: status 'Approved'
│   │   └── __init__.py           # Community migrations package marker
│   ├── admin.py                  # Admin interface for community posts & inquiries
│   ├── apps.py                   # Community app configuration
│   ├── forms.py                  # AdoptionPostForm, InquiryForm, StatusForm
│   ├── models.py                 # AdoptionPost & AdoptionInquiry models
│   ├── tests.py                  # Unit tests for community posts and approvals
│   ├── urls.py                   # Community board, post CRUD, & inquiry routes
│   ├── views.py                  # Community views, post management, inquiries
│   └── __init__.py               # Community app package marker
├── custom_admin/                 # Custom administrative panel (/admin-panel/)
│   ├── apps.py                   # CustomAdmin app configuration
│   ├── decorators.py             # Administrator and staff authentication guard
│   ├── forms.py                  # Forms for pets, products, orders, vets, and users
│   ├── tests.py                  # Unit tests for admin panel operations and CRUD
│   ├── urls.py                   # Routing table for /admin-panel/ modules
│   ├── views.py                  # Dashboard, CRUD views, and administrative logic
│   └── __init__.py               # CustomAdmin package marker
├── pets/                         # Foundation pets catalog, search, and favorites
│   ├── migrations/               # Database migrations for pets
│   │   ├── 0001_initial.py       # Initial Pet and Favorite models
│   │   ├── 0002_alter_pet_age.py # Migration: pet age as CharField
│   │   ├── 0003_pet_price_pet_price_type_alter_pet_age.py # Migration: price & price_type
│   │   └── __init__.py           # Pets migrations package marker
│   ├── admin.py                  # PetAdmin with pricing, age, and inventory controls
│   ├── api_urls.py               # REST API routes for pets
│   ├── api_views.py              # REST API ViewSet with token authentication
│   ├── apps.py                   # Pets app configuration
│   ├── models.py                 # Pet model (price, price_type, age text, status)
│   ├── serializers.py            # DRF serializers for pets and favorites
│   ├── tests.py                  # Unit tests for pet filters and pricing
│   ├── urls.py                   # Browse pets, pet details, toggle favorites
│   ├── views.py                  # Pet list (filtered by Available by default), detail
│   └── __init__.py               # Pets app package marker
├── store/                        # Pet accessories single-vendor e-commerce store
│   ├── management/               # Management commands for store
│   │   ├── commands/             # Custom Django management commands
│   │   │   ├── populate_store.py # Seed script for 20 pet accessory products
│   │   │   └── __init__.py       # Commands package marker
│   │   └── __init__.py           # Management package marker
│   ├── migrations/               # Database migrations for store
│   │   ├── 0001_initial.py       # Product, Order, and OrderItem models migration
│   │   └── __init__.py           # Store migrations package marker
│   ├── admin.py                  # Product catalog CRUD and Order management
│   ├── apps.py                   # Store app configuration
│   ├── forms.py                  # Checkout form with phone validation
│   ├── models.py                 # Product, Order, and OrderItem models
│   ├── tests.py                  # Unit tests for cart, checkout, stock deduction
│   ├── urls.py                   # Store catalog, cart, checkout, receipt routes
│   ├── views.py                  # Store views, cart session, orders, receipts
│   └── __init__.py               # Store app package marker
├── vets/                         # 24/7 veterinary directory with real-time shift system
│   ├── management/               # Management commands for vets
│   │   ├── commands/             # Custom Django management commands
│   │   │   ├── populate_vets.py  # Seed script for 6 vets across 3 shifts
│   │   │   └── __init__.py       # Commands package marker
│   │   └── __init__.py           # Management package marker
│   ├── migrations/               # Database migrations for vets
│   │   ├── 0001_initial.py       # Vet model migration
│   │   └── __init__.py           # Vets migrations package marker
│   ├── admin.py                  # Vet directory admin management
│   ├── apps.py                   # Vets app configuration
│   ├── models.py                 # Vet model (shifts, contacts, specialization)
│   ├── tests.py                  # Unit tests for clock-based shift detection
│   ├── urls.py                   # Vet directory routes
│   ├── views.py                  # Clock-based shift matching and vet list view
│   └── __init__.py               # Vets app package marker
├── static/                       # Static assets
│   ├── css/                      # Stylesheets
│   │   └── style.css             # "Deep Breath" palette tokens, layout & dark mode
│   └── js/                       # Client-side JavaScript
│       └── main.js               # Theme toggle, favorite handler, auto-dismiss
├── templates/                    # HTML Django templates
│   ├── accounts/                 # Authentication & profile templates
│   │   ├── edit_profile.html     # Profile editing view with phone/email validation
│   │   ├── forgot_password.html  # Profile verification password recovery form
│   │   ├── login.html            # User login with link to forgot password
│   │   ├── profile.html          # User profile dashboard
│   │   ├── register.html         # User registration with password strength meter
│   │   └── reset_password_direct.html # Set new password with live strength meter
│   ├── adoptions/                # Foundation adoption templates
│   │   ├── apply.html            # Pet adoption application form
│   │   └── my_requests.html      # Unified requests (Foundation & Community)
│   ├── community/                # Community rehoming templates
│   │   ├── inquiry_form.html     # Community adoption inquiry submission form
│   │   ├── my_inquiries.html     # Inquiries submitted to other pet owners
│   │   ├── my_posts.html         # Rehoming posts created by logged-in user
│   │   ├── post_confirm_delete.html # Confirmation modal for post deletion
│   │   ├── post_detail.html      # Community pet post detail view
│   │   ├── post_form.html        # Create/edit community pet post
│   │   ├── post_inquiries.html   # Owner inquiry review with 'Approved' option
│   │   ├── post_list.html        # Community pet rehoming board
│   │   └── public_profile.html   # Public profile showing user's pet posts
│   ├── custom_admin/             # Custom admin panel templates
│   │   ├── adoptions/            # Adoption applications review and deletion
│   │   │   ├── adoption_confirm_delete.html
│   │   │   ├── adoption_detail.html
│   │   │   └── adoption_list.html
│   │   ├── community/            # Community posts & inquiries moderation
│   │   │   ├── inquiry_confirm_delete.html
│   │   │   ├── inquiry_detail.html
│   │   │   ├── inquiry_list.html
│   │   │   ├── post_confirm_delete.html
│   │   │   └── post_list.html
│   │   ├── pets/                 # Pet listings management
│   │   │   ├── pet_confirm_delete.html
│   │   │   ├── pet_form.html
│   │   │   └── pet_list.html
│   │   ├── store/                # Accessories catalog and customer orders
│   │   │   ├── order_confirm_delete.html
│   │   │   ├── order_detail.html
│   │   │   ├── order_list.html
│   │   │   ├── product_confirm_delete.html
│   │   │   ├── product_form.html
│   │   │   └── product_list.html
│   │   ├── users/                # User accounts administration
│   │   │   ├── user_confirm_delete.html
│   │   │   ├── user_form.html
│   │   │   └── user_list.html
│   │   ├── base_admin.html       # Admin sidebar layout and top bar
│   │   ├── dashboard.html        # KPI statistics overview and recent activity
│   │   └── login.html            # Dedicated administrator sign-in portal
│   ├── pets/                     # Foundation pets templates
│   │   ├── pet_detail.html       # Pet detail with adoption fee & price type
│   │   └── pet_list.html         # Filtered by Available pets by default
│   ├── store/                    # Pet accessories store templates
│   │   ├── cart.html             # Shopping cart view with quantity adjustment
│   │   ├── checkout.html         # Shipping address & payment selection (COD/Online)
│   │   ├── my_orders.html        # Order history with direct receipt download links
│   │   ├── order_detail.html     # Order confirmation and invoice breakdown
│   │   ├── product_detail.html   # Accessory detail view with stock status
│   │   ├── receipt.html          # Digital PDF receipt with print/save button
│   │   └── store_home.html       # Store catalog with categories and search
│   ├── vets/                     # Veterinary care templates
│   │   └── vet_list.html         # Real-time clock & shift availability status
│   └── base.html                 # Master layout template with top navigation
├── yeager_adoption/              # Django core configuration package
│   ├── asgi.py                   # ASGI application entrypoint
│   ├── settings.py               # Application settings, middleware, databases
│   ├── urls.py                   # Top-level URL routing table (routes /admin-panel/)
│   ├── wsgi.py                   # WSGI application entrypoint with Vercel 'app'
│   └── __init__.py               # Core package marker
├── .gitignore                    # Git ignore file for Python, Django, IDEs
├── build_files.sh                # Vercel build script (pip, collectstatic, migrate)
├── db.sqlite3                    # SQLite database with dummy data
├── manage.py                     # Django administrative command-line utility
├── README.md                     # Comprehensive project documentation
├── requirements.txt              # Python production dependencies
└── vercel.json                   # Vercel serverless deployment configuration
```

---

## Key Features & Enhancements

### 1. "Deep Breath Like This" Color Palette
- Replaced bright colors with the **"Deep Breath"** color scheme (derived from Behr S460-7 *Deep Breath* `#395865`, accompanied by `#273e48`, `#52798a`, and soothing muted teal breath accent `#8cb7b2`).
- **Dark Mode Uniformity**: In dark mode, the top navigation bar and hero banner match seamlessly in `#10181c` (`var(--nav-bg)`), providing a relaxing, eye-friendly experience.

### 2. Mobile Phone and Email Formatting Validation
- Integrated strict input formatting checks across registration, profile editing, adoption inquiries, store checkout, and administrative forms:
  - **Phone Format**: Must match standard 11-digit mobile format (`01XXXXXXXXX` or `+8801XXXXXXXXX` with valid operator prefix).
  - **Email Format**: Strict RFC-compliant email validation requiring a valid mailbox, `@` delimiter, domain, and TLD.

### 3. Profile-Verification Password Recovery (No Email Console)
- Replaced the console-token email flow with a simple, secure **Profile-Verification** recovery workflow:
  1. User navigates to `/accounts/forgot-password/` and inputs their registered **Username** or **Email**.
  2. The system verifies that the account exists in the database.
  3. Upon verification, the user is directly redirected to the reset password page (`/accounts/reset-password/`).
  4. The user sets a new password with the interactive password strength meter.
  5. The password is encrypted and updated immediately; the user is redirected to login.

### 4. Password Strength Checking & Enforcement
- Evaluates 5 criteria: (1) 8+ characters, (2) uppercase letter, (3) lowercase letter, (4) numeric digit, (5) special symbol.
- Requires **Strong** or **Very Strong** (at least 4 criteria met). Weak and medium passwords are strictly rejected.

### 5. Flexible Pet Age Field
- Changed the `age` field across both store and community listings to a flexible text field (`CharField(max_length=50)`). Accepts natural inputs such as `"2 years 3 months"`, `"2 years"`, or `"3 months"`.

### 6. Default "Available" Pets Filter
- Store pet listings (`/pets/` and homepage) default to showing pets with status **Available**.

### 7. Adoption Inquiries "Approved" Status
- The community inquiries dropdown status `"Contacted"` has been updated to **`"Approved"`**.

### 8. Store Pet Pricing (Fixed vs Negotiable)
- Pet models support adoption fees in BDT and define whether the price is **Fixed Price** or **Negotiable**.

### 9. Pet Accessories E-Commerce Store
- Complete single-vendor shop selling cages, identification belts, care books, foods, ropes, grooming brushes, nail cutters, soaps, shampoos, and more.
- Real-time inventory tracking: ordering reduces stock; reaching `0` automatically shows **Out of Stock**.
- Cash on Delivery (COD) or Online Payment (instant dummy gateway).
- Digital receipt with a one-click **"Print / Save as PDF"** button.

### 10. 24/7 Clock-Based Veterinary Shift Directory
- 3 eight-hour shifts: Morning (6AM–2PM), Mid (2PM–10PM), and Night (10PM–6AM).
- Automatically accesses local time (`Asia/Dhaka`) and highlights the on-duty doctors with a pulsing badge.

---

## Running the Automated Test Suite

Run the full test suite across accounts, custom admin, pets, store, vets, and community apps:
```bash
python manage.py test
```

Expected output:
```text
Ran 24 tests in ...s

OK
```

---

## Deploying to Vercel

The application is pre-configured for deployment on **Vercel** serverless infrastructure (`vercel.json`, `build_files.sh`, `wsgi.py`).

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

---

## License

This project is licensed under the MIT License.
