import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Solution Center - Find Any Service",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define color theme - pure blue and white palette
COLORS = {
    "primary": "#1E88E5",       # Primary blue
    "secondary": "#90CAF9",     # Light blue
    "background": "#E3F2FD",    # Very light blue background
    "text": "#0D47A1",          # Dark blue text
    "accent": "#64B5F6",        # Accent blue
    "white": "#FFFFFF"
}

# Initialize session state
if 'selected_service' not in st.session_state:
    st.session_state.selected_service = None
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False

# Sample data for services
SAMPLE_SERVICES = [
    {
        "name": "Salone Elite Tailoring",
        "category": "Fashion & Clothing",
        "subcategory": "Tailoring",
        "city": "Freetown",
        "area": "Aberdeen",
        "district": "Western Area Urban",
        "country": "Sierra Leone",
        "gender_served": "All",
        "phone": "+232-76-123-456",
        "email": "info@saloneelite.sl",
        "rating": 4.8,
        "price_range": "$$",
        "description": "Premium tailoring services for men and women. Custom suits, traditional wear, and geles for special occasions.",
        "services": ["Custom Suits", "Traditional Wear", "Gele Tying", "Wedding Outfits", "Kaba & Slits"]
    },
    {
        "name": "Kamara Car Rentals",
        "category": "Transportation",
        "subcategory": "Car Rental",
        "city": "Freetown",
        "area": "Lumley",
        "district": "Western Area Urban",
        "country": "Sierra Leone",
        "gender_served": "All",
        "phone": "+232-88-765-432",
        "email": "bookings@kamaracars.sl",
        "rating": 4.5,
        "price_range": "$$$",
        "description": "Reliable car rental services with well-maintained vehicles. Airport transfers and city tours available.",
        "services": ["Economy Cars", "SUVs", "Lungi Airport Transfers", "City Tours", "Wedding Cars"]
    },
    {
        "name": "Aminata Beauty Palace",
        "category": "Beauty & Wellness",
        "subcategory": "Hair Salon",
        "city": "Bo",
        "area": "Bo Town Center",
        "district": "Bo District",
        "country": "Sierra Leone",
        "gender_served": "Women",
        "phone": "+232-76-456-789",
        "email": "aminata@beautypalace.sl",
        "rating": 4.9,
        "price_range": "$$",
        "description": "Full-service beauty salon specializing in natural hair care, braiding, and traditional Sierra Leonean styles.",
        "services": ["Natural Hair Care", "Braiding", "Locs Maintenance", "Makeup", "Henna Designs"]
    },
    {
        "name": "TechFix Salone",
        "category": "Technology",
        "subcategory": "Computer Repair",
        "city": "Freetown",
        "area": "Congo Cross",
        "district": "Western Area Urban",
        "country": "Sierra Leone",
        "gender_served": "All",
        "phone": "+232-77-123-456",
        "email": "support@techfixsalone.sl",
        "rating": 4.6,
        "price_range": "$",
        "description": "Professional computer and mobile device repair services. Software installation and data recovery.",
        "services": ["Laptop Repair", "Phone Repair", "Data Recovery", "Software Installation", "CCTV Setup"]
    },
    {
        "name": "Mama Fatmata Kitchen",
        "category": "Food & Catering",
        "subcategory": "Catering",
        "city": "Kenema",
        "area": "Kenema City",
        "district": "Kenema District",
        "country": "Sierra Leone",
        "gender_served": "All",
        "phone": "+232-76-987-654",
        "email": "orders@mamafatmata.sl",
        "rating": 4.7,
        "price_range": "$$",
        "description": "Authentic Sierra Leonean cuisine for events and daily meals. Specializing in jollof rice, cassava leaves, and groundnut soup.",
        "services": ["Event Catering", "Daily Meals", "Traditional Dishes", "Wedding Catering", "Corporate Lunch"]
    },
    {
        "name": "Green Hills Landscaping",
        "category": "Home & Garden",
        "subcategory": "Landscaping",
        "city": "Freetown",
        "area": "Hill Station",
        "district": "Western Area Rural",
        "country": "Sierra Leone",
        "gender_served": "All",
        "phone": "+232-88-234-567",
        "email": "info@greenhills.sl",
        "rating": 4.4,
        "price_range": "$$$",
        "description": "Professional landscaping and garden maintenance services for residential and commercial properties.",
        "services": ["Garden Design", "Lawn Maintenance", "Tree Planting", "Irrigation Systems", "Compound Cleaning"]
    }
]

# Service categories
SERVICE_CATEGORIES = {
    "Fashion & Clothing": ["Tailoring", "Shoe Repair", "Dry Cleaning", "Fashion Design", "Gele Tying"],
    "Transportation": ["Car Rental", "Taxi Service", "Logistics", "Moving Services", "Okada", "Poda Poda"],
    "Beauty & Wellness": ["Hair Salon", "Barber Shop", "Spa", "Fitness Center", "Massage Therapy"],
    "Technology": ["Computer Repair", "Phone Repair", "Web Development", "IT Support", "CCTV Installation"],
    "Food & Catering": ["Catering", "Restaurant", "Food Delivery", "Baking", "Street Food"],
    "Home & Garden": ["Landscaping", "Cleaning Service", "Plumbing", "Electrical", "Carpentry"],
    "Professional Services": ["Legal Services", "Accounting", "Consulting", "Real Estate"],
    "Education": ["Tutoring", "Training Centers", "Language Classes", "Skill Development"],
    "Health & Medical": ["Clinics", "Pharmacy", "Dental Care", "Traditional Healing"],
    "Entertainment": ["Event Planning", "Photography", "Music", "DJ Services"]
}

def get_css():
    return f"""
    <style>
        .stApp {{
            background-color: {COLORS["background"]};
        }}
        
        h1, h2, h3 {{
            color: {COLORS["text"]};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .main-header {{
            background-color: {COLORS["primary"]};
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .search-container {{
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 5px solid {COLORS["primary"]};
        }}
        
        .service-card {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid {COLORS["primary"]};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 450px !important;
            width: 100% !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }}
        
        .service-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .service-card-content {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        
        .service-name {{
            color: {COLORS["text"]};
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 8px;
            height: 45px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}
        
        .service-category {{
            background-color: {COLORS["secondary"]};
            color: {COLORS["text"]};
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            display: inline-block;
            margin-bottom: 10px;
            width: fit-content;
            font-weight: bold;
        }}
        
        .service-location {{
            color: {COLORS["text"]};
            font-weight: 500;
            margin-bottom: 8px;
            height: 20px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .service-rating {{
            color: #FF9800;
            font-weight: bold;
            margin-bottom: 10px;
            height: 20px;
        }}
        
        .service-description {{
            color: {COLORS["text"]};
            margin: 10px 0;
            height: 60px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            font-size: 0.9em;
        }}
        
        .service-services {{
            margin-bottom: 10px;
            height: 40px;
            overflow: hidden;
            font-size: 0.9em;
            color: {COLORS["text"]};
        }}
        
        .service-gender {{
            margin-bottom: 10px;
            height: 20px;
            font-size: 0.9em;
            color: {COLORS["text"]};
        }}
        
        .service-contact {{
            background-color: {COLORS["background"]};
            padding: 10px;
            border-radius: 8px;
            margin-top: auto;
            height: 60px;
            font-size: 0.85em;
            color: {COLORS["text"]};
        }}
        
        .click-indicator {{
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: {COLORS["primary"]};
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .stats-container {{
            display: flex;
            justify-content: space-around;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 5px solid {COLORS["primary"]};
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: {COLORS["primary"]};
        }}
        
        .stat-label {{
            color: {COLORS["text"]};
            font-size: 0.9em;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: {COLORS["text"]};
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 5px solid {COLORS["accent"]};
        }}
        
        .stButton>button {{
            background-color: {COLORS["primary"]} !important;
            color: white !important;
            border-radius: 5px !important;
            border: none !important;
            padding: 8px 16px !important;
            width: 100% !important;
            font-weight: bold !important;
            transition: background-color 0.3s !important;
        }}
        
        .stButton>button:hover {{
            background-color: {COLORS["text"]} !important;
        }}
        
        .product-gallery {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        
        .product-image {{
            width: 100%;
            height: 150px;
            background-color: {COLORS["background"]};
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
            color: {COLORS["primary"]};
            border: 2px solid {COLORS["accent"]};
            transition: transform 0.3s ease;
        }}
        
        .product-image:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        
        .product-label {{
            text-align: center;
            margin-top: 8px;
            font-weight: bold;
            color: {COLORS["text"]};
            font-size: 0.9em;
        }}
    </style>
    """

def get_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good Morning"
    elif current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def get_sample_products(service_category):
    """Get sample product images based on service category"""
    product_samples = {
        "Fashion & Clothing": [
            {"icon": "👔", "name": "Custom Suits"},
            {"icon": "👗", "name": "Traditional Wear"},
            {"icon": "👒", "name": "Accessories"},
            {"icon": "🧵", "name": "Alterations"},
            {"icon": "👜", "name": "Bags & Purses"},
            {"icon": "👠", "name": "Shoes & Footwear"}
        ],
        "Transportation": [
            {"icon": "🚗", "name": "Economy Cars"},
            {"icon": "🚙", "name": "SUVs"},
            {"icon": "🏍️", "name": "Motorcycles"},
            {"icon": "🚐", "name": "Vans"},
            {"icon": "🛻", "name": "Pickup Trucks"},
            {"icon": "🚕", "name": "Luxury Cars"}
        ],
        "Beauty & Wellness": [
            {"icon": "💇", "name": "Hair Styling"},
            {"icon": "💅", "name": "Nail Care"},
            {"icon": "💄", "name": "Makeup"},
            {"icon": "🧴", "name": "Hair Products"},
            {"icon": "🌿", "name": "Natural Treatments"},
            {"icon": "✨", "name": "Spa Services"}
        ],
        "Technology": [
            {"icon": "💻", "name": "Laptops"},
            {"icon": "📱", "name": "Mobile Phones"},
            {"icon": "🖥️", "name": "Desktop PCs"},
            {"icon": "📷", "name": "Cameras"},
            {"icon": "🎮", "name": "Gaming"},
            {"icon": "⌚", "name": "Smart Watches"}
        ],
        "Food & Catering": [
            {"icon": "🍛", "name": "Jollof Rice"},
            {"icon": "🥘", "name": "Traditional Dishes"},
            {"icon": "🎂", "name": "Cakes & Desserts"},
            {"icon": "🥤", "name": "Beverages"},
            {"icon": "🍖", "name": "Grilled Meats"},
            {"icon": "🥗", "name": "Salads & Sides"}
        ],
        "Home & Garden": [
            {"icon": "🌺", "name": "Flower Gardens"},
            {"icon": "🌳", "name": "Trees & Plants"},
            {"icon": "🏡", "name": "Landscaping"},
            {"icon": "🚿", "name": "Plumbing"},
            {"icon": "💡", "name": "Electrical"},
            {"icon": "🔨", "name": "Carpentry"}
        ]
    }
    
    return product_samples.get(service_category, [
        {"icon": "📦", "name": "Product 1"},
        {"icon": "📦", "name": "Product 2"},
        {"icon": "📦", "name": "Product 3"},
        {"icon": "📦", "name": "Product 4"},
        {"icon": "📦", "name": "Product 5"},
        {"icon": "📦", "name": "Product 6"}
    ])

def display_service_modal(service):
    """Display service details in a modal with product gallery"""
    if not st.session_state.show_modal or not service:
        return
    
    products = get_sample_products(service["category"])
    
    modal_html = f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.8); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 20px;">
        <div style="background-color: white; border-radius: 10px; padding: 30px; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="background-color: {COLORS['primary']}; color: white; padding: 20px; margin: -30px -30px 20px -30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h2>{service["name"]}</h2>
                <p>{service["category"]} - {service["subcategory"]}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <h3 style="color: {COLORS['text']}; margin-bottom: 15px;">📍 Location & Contact</h3>
                <div style="background-color: {COLORS['background']}; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <p><strong>Address:</strong> {service["area"]}, {service["city"]}, {service["district"]}</p>
                    <p><strong>Phone:</strong> {service["phone"]}</p>
                    <p><strong>Email:</strong> {service["email"]}</p>
                    <p><strong>Rating:</strong> {'⭐' * int(service["rating"])} {service["rating"]}/5.0</p>
                    <p><strong>Price Range:</strong> {service["price_range"]}</p>
                    <p><strong>Gender Served:</strong> {service["gender_served"]}</p>
                </div>
                
                <h3 style="color: {COLORS['text']}; margin-bottom: 15px;">📝 About This Service</h3>
                <div style="background-color: {COLORS['secondary']}; color: {COLORS['text']}; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <p>{service["description"]}</p>
                </div>
                
                <h3 style="color: {COLORS['text']}; margin-bottom: 15px;">🛍️ Services & Products</h3>
                <div style="margin-bottom: 20px;">
                    <p><strong>Available Services:</strong> {", ".join(service["services"])}</p>
                </div>
                
                <h3 style="color: {COLORS['text']}; margin-bottom: 15px;">📸 Sample Products/Services</h3>
                <div class="product-gallery">
    """
    
    for product in products:
        modal_html += f"""
                    <div>
                        <div class="product-image">{product["icon"]}</div>
                        <div class="product-label">{product["name"]}</div>
                    </div>
        """
    
    modal_html += """
                </div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(modal_html, unsafe_allow_html=True)

def display_service_card(service):
    """Display a service in a card format"""
    rating_stars = "⭐" * int(service["rating"])
    service_key = f"service_{service['name'].replace(' ', '_').replace('.', '_').replace(',', '_').replace("'", '_')}"
    
    card_html = f"""
    <div class="service-card">
        <div class="click-indicator">👁️</div>
        <div class="service-card-content">
            <div class="service-name">{service["name"]}</div>
            <div class="service-category">{service["category"]} - {service["subcategory"]}</div>
            <div class="service-location">📍 {service["area"]}, {service["city"]}, {service["district"]}</div>
            <div class="service-rating">{rating_stars} {service["rating"]}/5.0 | {service["price_range"]}</div>
            <div class="service-description">{service["description"]}</div>
            <div class="service-services"><strong>Services:</strong> {", ".join(service["services"])}</div>
            <div class="service-gender"><strong>Gender Served:</strong> {service["gender_served"]}</div>
            <div class="service-contact">
                <strong>Contact:</strong><br>
                📞 {service["phone"]}<br>
                📧 {service["email"]}
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if st.button(f"View Details", key=service_key, help=f"Click to view {service['name']} details"):
        st.session_state.selected_service = service
        st.session_state.show_modal = True
        st.rerun()

def filter_services(services, filters):
    """Filter services based on user criteria"""
    filtered = services.copy()
    
    if filters.get("search_query"):
        query = filters["search_query"].lower()
        filtered = [s for s in filtered if 
                   query in s["name"].lower() or 
                   query in s["description"].lower() or 
                   query in s["category"].lower()]
    
    if filters.get("category") and filters["category"] != "All Categories":
        filtered = [s for s in filtered if s["category"] == filters["category"]]
    
    if filters.get("district") and filters["district"] != "All Districts":
        filtered = [s for s in filtered if s["district"] == filters["district"]]
    
    if filters.get("city") and filters["city"] != "All Cities":
        filtered = [s for s in filtered if s["city"] == filters["city"]]
    
    if filters.get("gender") and filters["gender"] != "All":
        filtered = [s for s in filtered if s["gender_served"] in ["All", filters["gender"]]]
    
    if filters.get("min_rating"):
        filtered = [s for s in filtered if s["rating"] >= filters["min_rating"]]
    
    return filtered

def main():
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Header
    header_html = f"""
    <div class="main-header">
        <h1>🔍 Solution Center Sierra Leone</h1>
        <h3>Find Any Service, Anywhere, Anytime</h3>
        <p>{get_greeting()} | {datetime.now().strftime("%A, %B %d, %Y")}</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Statistics
    total_services = len(SAMPLE_SERVICES)
    total_categories = len(SERVICE_CATEGORIES)
    total_districts = len(set(s["district"] for s in SAMPLE_SERVICES))
    avg_rating = sum(s["rating"] for s in SAMPLE_SERVICES) / len(SAMPLE_SERVICES)
    
    stats_html = f"""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">{total_services}</div>
            <div class="stat-label">Services Listed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_categories}</div>
            <div class="stat-label">Categories</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_districts}</div>
            <div class="stat-label">Districts Covered</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{avg_rating:.1f}</div>
            <div class="stat-label">Avg Rating</div>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)
    
    # Search
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search for any service...", 
                                   placeholder="e.g., tailoring, car rental, beauty salon")
    with col2:
        search_button = st.button("Search", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filters
    with st.expander("🎯 Advanced Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ["All Categories"] + list(SERVICE_CATEGORIES.keys())
            selected_category = st.selectbox("Category", categories)
        
        with col2:
            districts = ["All Districts"] + sorted(list(set(s["district"] for s in SAMPLE_SERVICES)))
            selected_district = st.selectbox("District", districts)
            
            if selected_district != "All Districts":
                cities = ["All Cities"] + sorted([s["city"] for s in SAMPLE_SERVICES if s["district"] == selected_district])
            else:
                cities = ["All Cities"] + sorted(list(set(s["city"] for s in SAMPLE_SERVICES)))
            selected_city = st.selectbox("City", cities)
        
        with col3:
            selected_gender = st.selectbox("Gender Preference", ["All", "Men", "Women"])
            min_rating = st.select_slider("Minimum Rating", 
                                        options=[1.0, 2.0, 3.0, 4.0, 4.5, 5.0],
                                        value=1.0)
    
    # Apply filters
    filters = {
        "search_query": search_query,
        "category": selected_category,
        "district": selected_district,
        "city": selected_city,
        "gender": selected_gender,
        "min_rating": min_rating
    }
    
    filtered_services = filter_services(SAMPLE_SERVICES, filters)
    
    # Display results
    st.markdown(f"### Found {len(filtered_services)} service(s)")
    
    if filtered_services:
        for i in range(0, len(filtered_services), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                display_service_card(filtered_services[i])
            
            if i + 1 < len(filtered_services):
                with col2:
                    display_service_card(filtered_services[i + 1])
    else:
        no_results_html = """
        <div class="no-results">
            <h3>🔍 No Services Found</h3>
            <p>Try adjusting your search criteria or filters.</p>
        </div>
        """
        st.markdown(no_results_html, unsafe_allow_html=True)
    
    # Display modal
    if st.session_state.show_modal and st.session_state.selected_service:
        display_service_modal(st.session_state.selected_service)
        
        if st.button("❌ Close Details", type="secondary"):
            st.session_state.show_modal = False
            st.session_state.selected_service = None
            st.rerun()
    
    # Footer
    footer_html = f"""
    <div style="background-color: {COLORS['primary']}; color: white; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h4>Solution Center Sierra Leone</h4>
        <p>Your trusted directory for all services across Salone | © 2025</p>
        <p>📧 info@solutioncenter.sl | 📞 +232-76-SOLUTION</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
