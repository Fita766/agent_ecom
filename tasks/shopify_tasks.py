from crewai import Task
from agents.shopify_agents import (
    create_shopify_theme_builder_agent,
    create_product_page_creator_agent,
    create_landing_page_builder_agent,
    create_seo_optimizer_agent
)


def create_shopify_theme_task(context):
    """Task 11: Select and configure Shopify theme"""
    return Task(
        description="""
        For approved products, select and configure optimal Shopify theme:
        
        1. Get list of available themes from Shopify store
        2. Select theme based on product category:
           - Fashion: Elegant, image-focused themes
           - Tech/Gadgets: Modern, minimalist themes
           - Home/Garden: Clean, spacious themes
           - Beauty: Bright, vibrant themes
        3. Configure theme settings for conversion optimization
        4. Activate selected theme
        
        Theme selection criteria:
        - Matches product niche aesthetic
        - Mobile-responsive
        - Fast loading
        - Conversion-optimized layout
        
        Return theme selection and configuration details.
        """,
        agent=create_shopify_theme_builder_agent(),
        context=context,
        expected_output="""
        Theme configuration:
        - selected_theme_id
        - selected_theme_name
        - theme_activated (boolean)
        - configuration_settings (dict)
        """
    )


def create_product_page_task(context):
    """Task 12: Create product listing on Shopify"""
    return Task(
        description="""
        Create compelling product listing on Shopify for approved products:
        
        1. Write persuasive product title (SEO-optimized)
        2. Create detailed product description with:
           - Emotional triggers
           - Features and benefits
           - Social proof elements
           - Clear value proposition
        3. Set competitive pricing
        4. Upload product images (from source URLs)
        5. Add product variants if applicable
        6. Set product category and tags
        7. Configure inventory settings
        
        Product page must:
        - Be conversion-optimized
        - Include trust elements (guarantees, reviews)
        - Have clear CTAs
        - Be mobile-friendly
        
        Return created product details.
        """,
        agent=create_product_page_creator_agent(),
        context=context,
        expected_output="""
        Product page creation:
        - shopify_product_id
        - shopify_product_url
        - product_title
        - product_description
        - price_set
        - images_uploaded (count)
        - product_published (boolean)
        """
    )


def create_landing_page_task(context):
    """Task 13: Create high-converting landing page"""
    return Task(
        description="""
        Build custom landing page for approved products:
        
        1. Create compelling headline
        2. Write benefit-focused copy
        3. Add social proof (reviews, testimonials)
        4. Include urgency elements (limited time, stock)
        5. Design clear CTAs (Buy Now buttons)
        6. Add trust elements (guarantees, secure checkout badges)
        7. Optimize for mobile and desktop
        8. Structure content with visual hierarchy
        
        Landing page elements:
        - Hero section with product image
        - Benefits section
        - Social proof section
        - FAQ section
        - Final CTA section
        
        Return landing page details.
        """,
        agent=create_landing_page_builder_agent(),
        context=context,
        expected_output="""
        Landing page creation:
        - landing_page_url
        - landing_page_created (boolean)
        - sections_created (list)
        - conversion_elements_added (list)
        """
    )


def create_seo_optimization_task(context):
    """Task 14: Optimize for search engines"""
    return Task(
        description="""
        Optimize product pages and store for SEO:
        
        1. Research and select target keywords
        2. Optimize product title (include primary keyword)
        3. Write SEO-friendly meta description
        4. Optimize image alt tags
        5. Structure content with proper headings (H1, H2, H3)
        6. Add internal linking
        7. Create SEO-friendly URLs
        8. Add structured data (Schema.org markup)
        
        SEO optimization includes:
        - Keyword research
        - On-page optimization
        - Technical SEO
        - Content optimization
        
        Return SEO optimization details.
        """,
        agent=create_seo_optimizer_agent(),
        context=context,
        expected_output="""
        SEO optimization:
        - target_keywords (list)
        - meta_title_optimized
        - meta_description_optimized
        - image_alt_tags_added (count)
        - structured_data_added (boolean)
        - seo_score_improvement (estimated)
        """
    )
