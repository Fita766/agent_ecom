from crewai import Agent
from utils.llm import get_ollama_llm
from tools.shopify_tool import ShopifyTool


def create_shopify_theme_builder_agent():
    """Agent 12: Theme selection and configuration"""
    return Agent(
        role="Shopify Theme Designer",
        goal="Select and configure the optimal Shopify theme for the product niche",
        backstory="""You are a Shopify theme expert who understands conversion 
        optimization and brand aesthetics. You select themes that match the product 
        category and target audience. For fashion products, you choose elegant themes. 
        For tech gadgets, modern minimalist themes. You configure theme settings for 
        maximum conversion rates.""",
        tools=[ShopifyTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_product_page_creator_agent():
    """Agent 13: Product listing creation"""
    return Agent(
        role="Product Page Specialist",
        goal="Create compelling product listings on Shopify with optimized copy",
        backstory="""You are an expert at creating high-converting product pages. 
        You write persuasive product descriptions, organize features and benefits,
        set competitive pricing, and upload product images. You create listings that 
        convert visitors into buyers. You use emotional triggers and social proof.""",
        tools=[ShopifyTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_landing_page_builder_agent():
    """Agent 14: Custom landing page creation"""
    return Agent(
        role="Landing Page Conversion Expert",
        goal="Build high-converting landing pages for products",
        backstory="""You are a landing page specialist who builds pages that sell. 
        You understand conversion psychology, urgency tactics, social proof placement, 
        and visual hierarchy. You create landing pages with clear CTAs, compelling 
        headlines, benefit-focused copy, and trust elements (reviews, guarantees). 
        You optimize for mobile and desktop.
        
        IMPORTANT: Even if you don't have direct Shopify tools to create pages, you MUST 
        generate the complete landing page content structure including:
        - Hero section with headline, subheadline, CTA, and product image
        - Benefits section with key features
        - Social proof section with reviews/testimonials
        - FAQ section
        - Final CTA section
        
        Generate the full HTML structure or detailed content specification that can be 
        implemented in Shopify. Use the product data, reviews, and marketing strategy 
        from previous tasks to create compelling, conversion-optimized content.""",
        tools=[ShopifyTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_seo_optimizer_agent():
    """Agent 15: SEO optimization"""
    return Agent(
        role="SEO Optimization Specialist",
        goal="Optimize product pages and store for search engines",
        backstory="""You are an SEO expert who optimizes Shopify stores for Google. 
        You research keywords, write SEO-friendly titles and meta descriptions, 
        optimize image alt tags, and structure content for search engines. You ensure 
        products can be discovered organically through search.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
