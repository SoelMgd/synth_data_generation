import random
import argparse
import string
import json
from pathlib import Path
from .types import HTMLValidationProblem
from .verify import validate_html_with_external_tool

def generate_random_text(min_words: int = 3, max_words: int = 10) -> str:
    """Generate random text for content."""
    words = [
        'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
        'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
        'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
        'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
        'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
        'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
        'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
        'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum'
    ]
    
    num_words = random.randint(min_words, max_words)
    selected_words = random.sample(words, min(num_words, len(words)))
    return ' '.join(selected_words).capitalize()

def generate_random_id() -> str:
    """Generate a random HTML ID."""
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def generate_random_class() -> str:
    """Generate random CSS class names."""
    prefixes = ['btn', 'card', 'nav', 'form', 'text', 'bg', 'border', 'shadow', 'rounded']
    suffixes = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
    
    classes = []
    for _ in range(random.randint(1, 3)):
        if random.choice([True, False]):
            classes.append(f"{random.choice(prefixes)}-{random.choice(suffixes)}")
        else:
            classes.append(random.choice(prefixes))
    
    return ' '.join(classes)

def generate_navigation() -> str:
    """Generate a complex navigation component."""
    nav_items = ['Home', 'Products', 'Services', 'About', 'Contact', 'Blog', 'Support']
    selected_items = random.sample(nav_items, random.randint(4, 6))
    
    nav_html = f'''
    <nav class="{generate_random_class()}" role="navigation" aria-label="Main navigation">
        <div class="container-fluid">
            <a class="navbar-brand" href="/" aria-label="Company Home">
                <img src="/logo.svg" alt="Company Logo" width="{random.randint(120, 180)}" height="{random.randint(40, 60)}">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">'''
    
    for i, item in enumerate(selected_items):
        is_active = i == 0
        has_dropdown = random.choice([True, False]) and i < 3
        
        if has_dropdown:
            dropdown_id = generate_random_id()
            nav_html += f'''
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle{' active' if is_active else ''}" href="#" id="{dropdown_id}" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {item}
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="{dropdown_id}">'''
            
            for j in range(random.randint(2, 4)):
                nav_html += f'''
                            <li><a class="dropdown-item" href="/{item.lower()}/sub{j+1}">{item} Sub {j+1}</a></li>'''
            
            nav_html += '''
                        </ul>
                    </li>'''
        else:
            nav_html += f'''
                    <li class="nav-item">
                        <a class="nav-link{' active' if is_active else ''}" href="/{item.lower()}">{item}</a>
                    </li>'''
    
    nav_html += '''
                </ul>
            </div>
        </div>
    </nav>'''
    
    return nav_html

def generate_form_component() -> str:
    """Generate a complex form component."""
    form_types = ['contact', 'registration', 'newsletter', 'feedback', 'order']
    form_type = random.choice(form_types)
    form_id = generate_random_id()
    
    form_html = f'''
    <form class="{generate_random_class()}" id="{form_id}" method="post" action="/{form_type}" novalidate>
        <input type="hidden" name="csrf_token" value="{''.join(random.choices(string.ascii_letters + string.digits, k=32))}">
        <input type="hidden" name="form_type" value="{form_type}">'''
    
    field_types = [
        ('text', 'name', 'Full Name', True),
        ('email', 'email', 'Email Address', True),
        ('tel', 'phone', 'Phone Number', False),
        ('text', 'company', 'Company Name', False),
        ('url', 'website', 'Website URL', False)
    ]
    
    selected_fields = random.sample(field_types, random.randint(3, 5))
    
    for field_type, field_name, field_label, required in selected_fields:
        field_id = generate_random_id()
        form_html += f'''
        <div class="form-group mb-3">
            <label for="{field_id}" class="form-label{' required' if required else ''}">{field_label}</label>
            <input type="{field_type}" id="{field_id}" name="{field_name}" class="form-control" {'required' if required else ''} 
                   placeholder="Enter your {field_label.lower()}" 
                   {'minlength="2" maxlength="100"' if field_type == 'text' else ''}>
            <div class="invalid-feedback">Please provide a valid {field_label.lower()}.</div>
        </div>'''
    
    if random.choice([True, False]):
        select_id = generate_random_id()
        options = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5']
        selected_options = random.sample(options, random.randint(3, 5))
        
        form_html += f'''
        <div class="form-group mb-3">
            <label for="{select_id}" class="form-label">Select Category</label>
            <select id="{select_id}" name="category" class="form-select" required>
                <option value="">Choose an option</option>'''
        
        for option in selected_options:
            form_html += f'''
                <option value="{option.lower().replace(' ', '-')}">{option}</option>'''
        
        form_html += '''
            </select>
            <div class="invalid-feedback">Please select a category.</div>
        </div>'''
    
    if random.choice([True, False]):
        textarea_id = generate_random_id()
        form_html += f'''
        <div class="form-group mb-3">
            <label for="{textarea_id}" class="form-label">Message</label>
            <textarea id="{textarea_id}" name="message" class="form-control" rows="{random.randint(3, 6)}" 
                      placeholder="Enter your message here..." minlength="10" maxlength="1000"></textarea>
            <div class="form-text">Maximum 1000 characters.</div>
        </div>'''
    
    if random.choice([True, False]):
        checkbox_type = random.choice(['checkbox', 'radio'])
        group_name = 'preferences' if checkbox_type == 'checkbox' else 'choice'
        
        form_html += f'''
        <div class="form-group mb-3">
            <fieldset>
                <legend class="form-label">Select {group_name.title()}</legend>'''
        
        for i in range(random.randint(2, 4)):
            option_id = generate_random_id()
            form_html += f'''
                <div class="form-check">
                    <input class="form-check-input" type="{checkbox_type}" name="{group_name}" id="{option_id}" value="option{i+1}">
                    <label class="form-check-label" for="{option_id}">
                        {generate_random_text(2, 4)}
                    </label>
                </div>'''
        
        form_html += '''
            </fieldset>
        </div>'''
    
    form_html += f'''
        <div class="form-actions">
            <button type="submit" class="{generate_random_class()}">
                <i class="fas fa-paper-plane me-2"></i>
                Submit {form_type.title()}
            </button>
            <button type="reset" class="btn btn-secondary ms-2">
                <i class="fas fa-undo me-2"></i>
                Reset
            </button>
        </div>
    </form>'''
    
    return form_html

def generate_card_grid() -> str:
    """Generate a grid of cards with various content."""
    num_cards = random.randint(3, 8)
    grid_html = """<div class="row g-4">"""
    
    for i in range(num_cards):
        card_id = generate_random_id()
        has_image = random.choice([True, False])
        has_footer = random.choice([True, False])
        
        grid_html += f'''
        <div class="col-lg-{random.choice([3, 4, 6])} col-md-6">
            <div class="card {generate_random_class()}" id="{card_id}">'''
        
        if has_image:
            grid_html += f'''
                <img src="/images/card-{i+1}.jpg" class="card-img-top" alt="Card image {i+1}" loading="lazy" width="{random.randint(300, 500)}" height="{random.randint(200, 300)}">'''
        
        grid_html += f'''
                <div class="card-body">
                    <h5 class="card-title">{generate_random_text(2, 5)}</h5>
                    <p class="card-text">{generate_random_text(10, 25)}</p>'''
        
        if random.choice([True, False]):
            grid_html += f'''
                    <div class="card-meta mb-2">
                        <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>
                            {random.choice(['January', 'February', 'March', 'April', 'May'])} {random.randint(1, 28)}, 2024
                        </small>
                    </div>'''
        
        if random.choice([True, False]):
            grid_html += """<div class="card-tags mb-2">"""
            for j in range(random.randint(1, 3)):
                grid_html += f'''
                        <span class="badge bg-{random.choice(['primary', 'secondary', 'success', 'info'])}">{generate_random_text(1, 2)}</span>'''
            grid_html += '''
                    </div>'''
        
        grid_html += f'''
                    <a href="/details/{card_id}" class="btn btn-{random.choice(['primary', 'outline-primary', 'secondary'])}">
                        {random.choice(['Read More', 'Learn More', 'View Details', 'Explore'])}
                    </a>
                </div>'''
        
        if has_footer:
            grid_html += f'''
                <div class="card-footer text-muted">
                    <small>{generate_random_text(3, 8)}</small>
                </div>'''
        
        grid_html += '''
            </div>
        </div>'''
    
    grid_html += '''
    </div>'''
    
    return grid_html

def generate_complex_html_by_theme(theme: str) -> str:
    """Generate complex HTML based on theme."""
    
    themes_config = {
        'ecommerce': {
            'title': 'Premium E-commerce Store',
            'components': ['navigation', 'hero', 'product_grid', 'features', 'testimonials', 'newsletter'],
            'css_framework': 'bootstrap',
            'color_scheme': 'primary'
        },
        'blog': {
            'title': 'Professional Blog Platform',
            'components': ['navigation', 'hero', 'article_grid', 'sidebar', 'comments', 'newsletter'],
            'css_framework': 'bootstrap',
            'color_scheme': 'info'
        },
        'corporate': {
            'title': 'Corporate Business Solutions',
            'components': ['navigation', 'hero', 'services', 'team', 'contact_form', 'testimonials'],
            'css_framework': 'bootstrap',
            'color_scheme': 'dark'
        },
        'portfolio': {
            'title': 'Creative Portfolio Showcase',
            'components': ['navigation', 'hero', 'gallery', 'about', 'contact_form', 'social'],
            'css_framework': 'bootstrap',
            'color_scheme': 'success'
        },
        'dashboard': {
            'title': 'Analytics Dashboard Pro',
            'components': ['navigation', 'sidebar', 'stats', 'charts', 'tables', 'notifications'],
            'css_framework': 'bootstrap',
            'color_scheme': 'warning'
        }
    }
    
    config = themes_config.get(theme, themes_config['ecommerce'])
    
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}" class="no-js">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, maximum-scale=5.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="{generate_random_text(8, 15)} - Professional {theme} solution">
    <meta name="keywords" content="{', '.join([generate_random_text(1, 2) for _ in range(5)])}">
    <meta name="author" content="{generate_random_text(2, 3)} Solutions">
    <meta name="robots" content="index, follow, max-snippet:-1">
    <meta property="og:title" content="{config['title']}">
    <meta property="og:description" content="{generate_random_text(10, 20)}">
    <meta property="og:image" content="https://example.com/og-image.jpg">
    <meta property="og:type" content="website">
    <title>{config['title']} | {generate_random_text(3, 6)}</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org/",
        "@type": "WebSite",
        "name": "{config['title']}",
        "url": "https://example.com"
    }}
    </script>
</head>
<body class="{theme}-theme" data-page="{theme}">
    <a href="#main-content" class="skip-link sr-only sr-only-focusable">Skip to main content</a>
    
    <header class="main-header sticky-top bg-white shadow-sm" role="banner">
        {generate_navigation()}
    </header>

    <main id="main-content" class="main-content" role="main">'''
    
    # Theme-specific sections
    sections = random.sample(config['components'], random.randint(4, len(config['components'])))
    
    for i, section in enumerate(sections):
        section_id = generate_random_id()
        
        if section == 'hero':
            html += f'''
        <section class="hero-section bg-{config['color_scheme']} text-white py-5" id="{section_id}">
            <div class="container">
                <div class="row align-items-center min-vh-50">
                    <div class="col-lg-6">
                        <h1 class="display-4 fw-bold mb-4">{generate_random_text(4, 8)}</h1>
                        <p class="lead mb-4">{generate_random_text(15, 25)}</p>
                        <div class="hero-actions">
                            <a href="/get-started" class="btn btn-light btn-lg me-3">
                                <i class="fas fa-rocket me-2"></i>Get Started
                            </a>
                            <a href="/learn-more" class="btn btn-outline-light btn-lg">
                                <i class="fas fa-play-circle me-2"></i>Learn More
                            </a>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <img src="/images/hero-{theme}.jpg" alt="Hero image" class="img-fluid rounded shadow" loading="eager">
                    </div>
                </div>
            </div>
        </section>'''
        
        elif section in ['product_grid', 'article_grid', 'gallery']:
            html += f'''
        <section class="content-grid py-5" id="{section_id}">
            <div class="container">
                <div class="row mb-5">
                    <div class="col-lg-8 mx-auto text-center">
                        <h2 class="display-5 fw-bold mb-3">{generate_random_text(3, 6)}</h2>
                        <p class="lead text-muted">{generate_random_text(12, 20)}</p>
                    </div>
                </div>
                {generate_card_grid()}
            </div>
        </section>'''
        
        elif section == 'contact_form':
            html += f'''
        <section class="contact-section py-5 bg-light" id="{section_id}">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 mx-auto">
                        <div class="text-center mb-5">
                            <h2 class="display-5 fw-bold mb-3">{generate_random_text(2, 4)}</h2>
                            <p class="lead text-muted">{generate_random_text(10, 18)}</p>
                        </div>
                        <div class="card shadow border-0">
                            <div class="card-body p-5">
                                {generate_form_component()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''
        
        elif section == 'features':
            num_features = random.randint(3, 6)
            html += f'''
        <section class="features-section py-5" id="{section_id}">
            <div class="container">
                <div class="row mb-5">
                    <div class="col-lg-8 mx-auto text-center">
                        <h2 class="display-5 fw-bold mb-3">{generate_random_text(3, 5)}</h2>
                        <p class="lead text-muted">{generate_random_text(12, 20)}</p>
                    </div>
                </div>
                <div class="row g-4">'''
            
            icons = ['star', 'shield', 'rocket', 'heart', 'cog', 'chart-line', 'users', 'globe']
            for j in range(num_features):
                html += f'''
                    <div class="col-lg-4 col-md-6">
                        <div class="feature-item text-center p-4">
                            <div class="feature-icon mb-3">
                                <i class="fas fa-{random.choice(icons)} fa-3x text-{config['color_scheme']}"></i>
                            </div>
                            <h4 class="mb-3">{generate_random_text(2, 4)}</h4>
                            <p class="text-muted">{generate_random_text(8, 15)}</p>
                        </div>
                    </div>'''
            
            html += '''
                </div>
            </div>
        </section>'''
        
        elif section == 'testimonials':
            num_testimonials = random.randint(2, 4)
            html += f'''
        <section class="testimonials-section py-5 bg-light" id="{section_id}">
            <div class="container">
                <div class="row mb-5">
                    <div class="col-lg-8 mx-auto text-center">
                        <h2 class="display-5 fw-bold mb-3">{generate_random_text(3, 5)}</h2>
                        <p class="lead text-muted">{generate_random_text(10, 18)}</p>
                    </div>
                </div>
                <div class="row g-4">'''
            
            for j in range(num_testimonials):
                html += f'''
                    <div class="col-lg-{12 // num_testimonials} col-md-6">
                        <div class="testimonial-card card border-0 shadow h-100">
                            <div class="card-body p-4">
                                <div class="testimonial-rating mb-3">'''
                
                for star in range(5):
                    html += """<i class="fas fa-star text-warning"></i>"""
                
                html += f'''
                                </div>
                                <blockquote class="blockquote mb-3">
                                    <p>"{generate_random_text(15, 25)}"</p>
                                </blockquote>
                                <div class="testimonial-author d-flex align-items-center">
                                    <img src="/images/avatar-{j+1}.jpg" alt="Customer" class="rounded-circle me-3" width="50" height="50" loading="lazy">
                                    <div>
                                        <h6 class="mb-0">{generate_random_text(2, 3)}</h6>
                                        <small class="text-muted">{generate_random_text(2, 4)}</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>'''
            
            html += '''
                </div>
            </div>
        </section>'''
        
        elif section == 'newsletter':
            html += f'''
        <section class="newsletter-section py-5 bg-{config['color_scheme']} text-white" id="{section_id}">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 mx-auto text-center">
                        <h2 class="display-6 fw-bold mb-3">{generate_random_text(4, 7)}</h2>
                        <p class="lead mb-4">{generate_random_text(12, 20)}</p>
                        <form class="newsletter-form row g-3 justify-content-center" method="post" action="/newsletter">
                            <div class="col-md-6">
                                <input type="email" class="form-control form-control-lg" name="email" placeholder="Enter your email address" required>
                            </div>
                            <div class="col-md-auto">
                                <button type="submit" class="btn btn-light btn-lg">
                                    <i class="fas fa-paper-plane me-2"></i>Subscribe
                                </button>
                            </div>
                            <div class="col-12">
                                <small class="text-light opacity-75">
                                    <i class="fas fa-lock me-1"></i>
                                    {generate_random_text(8, 12)}
                                </small>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>'''
    
    # Footer
    html += f'''
    </main>

    <footer class="bg-dark text-light py-5" role="contentinfo">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4 col-md-6">
                    <h5 class="mb-3">{generate_random_text(1, 2)}</h5>
                    <p class="mb-3">{generate_random_text(12, 20)}</p>
                    <div class="social-links">'''
    
    social_networks = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']
    selected_social = random.sample(social_networks, random.randint(3, 5))
    
    for social in selected_social:
        html += f'''
                        <a href="https://{social}.com/company" class="text-light me-3" aria-label="{social.title()}" target="_blank" rel="noopener">
                            <i class="fab fa-{social} fa-lg" aria-hidden="true"></i>
                        </a>'''
    
    html += f'''
                    </div>
                </div>
                <div class="col-lg-2 col-md-6">
                    <h6 class="mb-3">{generate_random_text(1, 2)}</h6>
                    <ul class="list-unstyled">'''
    
    footer_links = ['About', 'Services', 'Products', 'Blog', 'Contact', 'Support', 'Careers']
    selected_links = random.sample(footer_links, random.randint(4, 6))
    
    for link in selected_links:
        html += f'''
                        <li class="mb-2"><a href="/{link.lower()}" class="text-light text-decoration-none">{link}</a></li>'''
    
    html += f'''
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h6 class="mb-3">{generate_random_text(1, 2)}</h6>
                    <address class="mb-0">
                        <p class="mb-1">
                            <i class="fas fa-map-marker-alt me-2"></i>
                            {random.randint(100, 9999)} {generate_random_text(2, 3)} Street
                        </p>
                        <p class="mb-1">
                            <i class="fas fa-phone me-2"></i>
                            +1 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}
                        </p>
                        <p class="mb-0">
                            <i class="fas fa-envelope me-2"></i>
                            contact@{generate_random_text(1, 2).replace(' ', '')}.com
                        </p>
                    </address>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h6 class="mb-3">{generate_random_text(2, 3)}</h6>
                    <p class="mb-3">{generate_random_text(8, 15)}</p>
                    <div class="newsletter-signup">
                        <form method="post" action="/footer-newsletter">
                            <div class="input-group">
                                <input type="email" class="form-control" name="email" placeholder="Your email" required>
                                <button class="btn btn-{config['color_scheme']}" type="submit">
                                    <i class="fas fa-arrow-right"></i>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <hr class="my-4">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <p class="mb-0">&copy; 2024 {generate_random_text(2, 3)} Solutions. All rights reserved.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <div class="footer-legal">'''
    
    legal_links = ['Privacy Policy', 'Terms of Service', 'Cookie Policy', 'Accessibility']
    selected_legal = random.sample(legal_links, random.randint(2, 4))
    
    for i, legal in enumerate(selected_legal):
        separator = ' | ' if i < len(selected_legal) - 1 else ''
        html += f'''
                        <a href="/{legal.lower().replace(' ', '-')}" class="text-light text-decoration-none">{legal}</a>{separator}'''
    
    html += '''
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/assets/js/main.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize tooltips
            const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
            
            // Form validation
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function(event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                });
            });
        });
    </script>
</body>
</html>'''
    
    return html

def introduce_html_error(valid_html: str) -> str:
    """Introduce a single subtle HTML error."""
    error_types = [
        'unclosed_tag',
        'malformed_attribute', 
        'invalid_nesting'
    ]
    
    error_type = random.choice(error_types)
    
    if error_type == 'unclosed_tag':
        # Find a tag to leave unclosed and remove it
        import re
        tag_pattern = r'<(\w+)[^>]*>.*?</\1>'
        matches = list(re.finditer(tag_pattern, valid_html, re.DOTALL))
        
        if matches:
            match = random.choice(matches)
            tag_name = match.group(1)
            closing_tag = f'</{tag_name}>'
            last_occurrence = valid_html.rfind(closing_tag, match.start(), match.end())
            if last_occurrence != -1:
                valid_html = valid_html[:last_occurrence] + valid_html[last_occurrence + len(closing_tag):]
    
    elif error_type == 'malformed_attribute':
        # Find an attribute to remove the closing quote
        import re
        attr_pattern = r'(\w+)="([^"]*)"'
        matches = list(re.finditer(attr_pattern, valid_html))
        
        if matches:
            match = random.choice(matches)
            malformed = f'{match.group(1)}="{match.group(2)}'
            valid_html = valid_html[:match.start()] + malformed + valid_html[match.end():]
    
    elif error_type == 'invalid_nesting':
        # Create invalid nesting like <p><div></div></p>
        import re
        p_pattern = r'<p[^>]*>(.*?)</p>'
        matches = list(re.finditer(p_pattern, valid_html, re.DOTALL))
        
        if matches:
            match = random.choice(matches)
            content = match.group(1)
            invalid_content = f'<div class="invalid-nesting">{content}</div>'
            valid_html = valid_html[:match.start(1)] + invalid_content + valid_html[match.end(1):]
    
    return valid_html

def generate_html_validation_problem() -> HTMLValidationProblem:
    """Generate an HTML validation problem (valid or invalid)."""
    
    themes = ['ecommerce', 'blog', 'corporate', 'portfolio', 'dashboard']
    theme = random.choice(themes)
    
    valid_html = generate_complex_html_by_theme(theme)
    
    is_valid, errors = validate_html_with_external_tool(valid_html)
    
    max_attempts = 3
    attempts = 0
    while not is_valid and attempts < max_attempts:
        print(f"  Warning: Generated HTML has validation errors, regenerating... (attempt {attempts + 1})")
        if errors:
            print(f"  Errors: {errors[:2]}") 
        valid_html = generate_complex_html_by_theme(theme)
        is_valid, errors = validate_html_with_external_tool(valid_html)
        attempts += 1
    
    if not is_valid:
        raise ValueError("Could not generate valid HTML after max attempts")
    
    # 50% valid, 50% invalid data sample
    should_be_valid = random.choice([True, False])
    
    if should_be_valid:
        return HTMLValidationProblem(
            html_string=valid_html,
            is_valid=True
        )
    else:
        if is_valid:
            invalid_html = introduce_html_error(valid_html)
            return HTMLValidationProblem(
                html_string=invalid_html,
                is_valid=False
            )
        else:
            return HTMLValidationProblem(
                html_string=valid_html,
                is_valid=False
            )

def main():
    parser = argparse.ArgumentParser(description="Generate HTML validation problems")
    parser.add_argument("--num-samples", type=int, default=10, help="Number of problems to generate")
    parser.add_argument("--output", type=str, default="format_validation/data/problems.jsonl", help="Output file path")
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    problems = []
    
    print(f"Generating {args.num_samples} HTML validation problems...")
    
    for i in range(args.num_samples):
        problem = generate_html_validation_problem()
        problems.append(problem.model_dump())
        
        if (i + 1) % 5 == 0 or (i + 1) == args.num_samples:
            print(f"Generated {i + 1}/{args.num_samples} problems")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for problem in problems:
            f.write(json.dumps(problem, ensure_ascii=False) + '\n')
    
    print(f"Saved {len(problems)} problems to {output_path}")
    
    valid_count = sum(1 for p in problems if p['is_valid'])
    invalid_count = len(problems) - valid_count
    
    print(f"Statistics:")
    print(f"  Valid HTML: {valid_count} ({valid_count/len(problems)*100:.1f}%)")
    print(f"  Invalid HTML: {invalid_count} ({invalid_count/len(problems)*100:.1f}%)")
    
    lengths = [len(p['html_string']) for p in problems]
    print(f"  Average HTML length: {sum(lengths)/len(lengths):.0f} characters")
    print(f"  Min/Max length: {min(lengths)}/{max(lengths)} characters")

if __name__ == "__main__":
    main() 