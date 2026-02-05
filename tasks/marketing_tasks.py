from crewai import Task
from agents.marketing_agents import (
    create_marketing_strategy_agent,
    create_tiktok_ads_agent,
    create_google_ads_agent,
    create_facebook_ads_agent
)


def create_marketing_strategy_task(context):
    """Task: Develop comprehensive marketing strategy"""
    return Task(
        description="""
        Develop a comprehensive marketing strategy for approved products:
        
        CRITICAL: Extract REAL data from previous tasks:
        - Task 6 (Review Analysis): Extract main_pros, main_cons, sentiment_score, red_flags
        - Task 2 (Market Analysis): Extract target_demographics, target_geographies, niche
        - Task 10 (Product Scoring): Extract strengths, weaknesses, overall_score
        - Task 8 (Pricing Strategy): Extract profit_margin_percent, suggested_retail_price
        
        For EACH approved product (from Task 11 decision task):
        
        1. Analyze customer reviews (from Task 6):
           - Extract EXACT pros from review analysis (e.g., "battery life", "sound quality")
           - Extract EXACT cons/objections (e.g., "shipping time", "durability concerns")
           - Identify emotional triggers from positive reviews
           - Note specific pain points mentioned in negative reviews
        
        2. Define core messaging (be SPECIFIC):
           - Primary value proposition: ONE clear sentence (e.g., "Premium sound quality at half the price")
           - Key selling points: List top 3-5 EXACT features from reviews (e.g., "30-hour battery", "IPX7 waterproof")
           - Unique differentiators: What makes this product different (from competitive analysis)
           - Emotional benefits: How customers FEEL (e.g., "peace of mind", "confidence", "freedom")
           - Functional benefits: What it DOES (e.g., "noise cancellation", "quick charge")
           - Brand voice: Specific tone (e.g., "friendly and approachable", "professional and trustworthy")
        
        3. Develop positioning strategy:
           - Target audience persona: SPECIFIC demographics (age, income, lifestyle, pain points)
           - Competitive positioning: Where this product sits vs competitors (e.g., "premium quality at mid-range price")
           - Price positioning: How to talk about price (e.g., "affordable luxury", "best value")
           - Market positioning statement: ONE sentence positioning (e.g., "For budget-conscious audiophiles who want premium sound without the premium price")
        
        4. Create messaging framework (be ACTIONABLE):
           - Headline variations: 10 SPECIFIC headlines ready to use (e.g., "Premium Sound, Half the Price")
           - Subheadline variations: 5 SPECIFIC subheadlines (e.g., "Experience crystal-clear audio with 30-hour battery life")
           - Key messages by channel:
             * Social media: 5 SPECIFIC posts ready to copy-paste
             * Email marketing: 3 SPECIFIC email subject lines and opening lines
             * Product landing: SPECIFIC copy for hero section, benefits section
           - Objection handling: SPECIFIC responses to common objections (e.g., "Worried about shipping? We offer free 2-day delivery")
           - Social proof messaging: How to use reviews (e.g., "Join 10,000+ satisfied customers")
        
        5. Content strategy (be SPECIFIC):
           - Product description focus: EXACT phrases to emphasize (e.g., "30-hour battery", "IPX7 waterproof")
           - Ad creative focus: SPECIFIC visuals to show (e.g., "product in water", "battery icon with 30h")
           - FAQ topics: 5 SPECIFIC questions to address (e.g., "How long does shipping take?", "Is it really waterproof?")
           - Review response strategy: How to respond to positive/negative reviews
        
        IMPORTANT:
        - Use REAL data from context, not generic statements
        - Be SPECIFIC and ACTIONABLE - every message should be ready to use
        - For EACH approved product, create a complete strategy
        - Return JSON format with all products
        
        Return comprehensive marketing strategy document in JSON format.
        """,
        agent=create_marketing_strategy_agent(),
        context=context,
        expected_output="""
        JSON object with marketing strategy for each approved product:
        {
          "Product Name": {
            "core_value_proposition": "One clear sentence",
            "key_selling_points": ["Exact feature 1", "Exact feature 2", ...],
            "target_audience_refinement": {
              "demographics": "Specific age, income, lifestyle",
              "pain_points": ["Specific pain 1", "Specific pain 2"],
              "motivations": ["Specific motivation 1", ...]
            },
            "positioning_statement": "One sentence positioning",
            "messaging_framework": {
              "headline_variations": ["Headline 1", "Headline 2", ...],
              "subheadline_variations": ["Subheadline 1", ...],
              "key_messages": {
                "social_media": ["Post 1", "Post 2", ...],
                "email_marketing": ["Subject line 1", ...],
                "product_landing": "Specific copy for landing page"
              },
              "objection_handling": {
                "objection_1": "Specific response",
                "objection_2": "Specific response"
              },
              "social_proof_messaging": "How to use reviews"
            },
            "content_strategy": {
              "product_description_focus": ["Exact phrase 1", ...],
              "ad_creative_focus": ["Visual 1", "Visual 2", ...],
              "faq_topics": ["Question 1", "Question 2", ...]
            },
            "review_insights_used": {
              "pros_from_reviews": ["Pro 1", "Pro 2", ...],
              "cons_from_reviews": ["Con 1", ...],
              "emotional_triggers": ["Trigger 1", ...]
            }
          },
          ...
        }
        """
    )


def create_tiktok_ads_campaign_task(context):
    """Task: Create TikTok advertising campaign"""
    return Task(
        description="""
        Create a complete TikTok advertising campaign for approved products:
        
        CRITICAL: Extract data from previous tasks:
        - Task 16 (Marketing Strategy): Use headline_variations, key_messages, target_audience
        - Task 1 (Trend Discovery): Use engagement_metrics, source_url for inspiration
        - Task 11 (Decision): Get list of approved products
        
        For EACH approved product, create EXACT campaign configuration:
        
        1. Campaign structure (EXACT values):
           - Campaign name: "ProductName_TikTok_Launch_2024"
           - Campaign objective: "Conversions" or "Traffic" (be specific)
           - Daily budget: EXACT amount (e.g., "$50/day")
           - Total budget: EXACT amount (e.g., "$1500 for 30 days")
           - Campaign duration: EXACT dates (e.g., "2024-02-01 to 2024-03-02")
           - Schedule: EXACT times (e.g., "7 days/week, 8AM-10PM EST")
        
        2. Audience targeting (EXACT settings):
           - Demographics: EXACT age range (e.g., "18-35"), gender, location
           - Interests: EXACT TikTok interest categories (e.g., "Tech", "Lifestyle", "Home Decor")
           - Behaviors: EXACT behaviors (e.g., "Engages with product videos", "Makes online purchases")
           - Lookalike audience: EXACT source (e.g., "Website visitors last 30 days", "Email subscribers")
           - Geographic targeting: EXACT countries/cities (e.g., "United States, Canada, United Kingdom")
           - Exclusions: EXACT exclusions (e.g., "Users who visited competitor sites")
        
        3. Ad creative strategy (READY TO USE):
           - Video concept: SPECIFIC concept (e.g., "Before/after showing product solving problem")
           - Hook (first 3 seconds): EXACT hook text (e.g., "POV: You finally found the perfect [product]")
           - Trending sounds: SPECIFIC sound names or hashtags (e.g., "#fyp", "#viral", trending audio track)
           - Visual style: SPECIFIC style (e.g., "Fast-paced cuts, bright lighting, user-generated feel")
           - Call-to-action: EXACT CTA text (e.g., "Shop Now", "Learn More", "Get 20% Off")
           - Ad copy variations: 5 EXACT captions ready to use (max 220 characters each)
        
        4. Campaign settings (EXACT configuration):
           - Ad placements: EXACT placements (e.g., ["In-Feed", "Spark Ads", "TopView"])
           - Bidding strategy: EXACT strategy (e.g., "Cost Per Click (CPC)", "Cost Per Action (CPA)")
           - Bid amount: EXACT bid (e.g., "$0.50 per click", "$5.00 per conversion")
           - Optimization goals: EXACT goals (e.g., "Conversions", "Click-through rate")
           - A/B testing plan: SPECIFIC test groups (e.g., "Test A: Hook variation 1, Test B: Hook variation 2")
        
        5. Creative brief (DETAILED and ACTIONABLE):
           - Video script: EXACT script with timestamps (e.g., "0-3s: Hook, 4-10s: Problem, 11-20s: Solution")
           - Key visuals: SPECIFIC shots to include (e.g., "Product in use", "Close-up of key feature")
           - Text overlays: EXACT text for each overlay (e.g., "30-Hour Battery", "IPX7 Waterproof")
           - Product showcase moments: EXACT timestamps (e.g., "Show product at 5s, 15s, 25s")
           - Music/sound: SPECIFIC recommendation (e.g., "Trending audio: [name], or upbeat instrumental")
        
        IMPORTANT:
        - Be EXACT and ACTIONABLE - every setting should be ready to configure in TikTok Ads Manager
        - Use REAL data from marketing strategy task
        - For EACH approved product, create complete campaign
        - Return JSON format with all products
        
        Return complete TikTok campaign plan in JSON format with EXACT configuration values.
        """,
        agent=create_tiktok_ads_agent(),
        context=context,
        expected_output="""
        JSON object with TikTok campaign for each approved product:
        {
          "Product Name": {
            "campaign_name": "Exact campaign name",
            "campaign_objective": "Conversions or Traffic",
            "budget_recommendation": {
              "daily_budget": "$50",
              "total_budget": "$1500",
              "duration_days": 30
            },
            "target_audience": {
              "demographics": {
                "age": "18-35",
                "gender": "All",
                "location": "United States, Canada, United Kingdom"
              },
              "interests": ["Exact interest 1", "Exact interest 2"],
              "behaviors": ["Exact behavior 1", ...],
              "lookalike_audience": "Exact source",
              "geographic_targeting": ["Country 1", "Country 2"]
            },
            "ad_creative_strategy": {
              "video_concept": "Specific concept description",
              "hook_ideas": ["Exact hook 1", "Exact hook 2", ...],
              "trending_sounds_recommendations": ["Sound 1", ...],
              "ad_copy_variations": ["Exact caption 1", "Exact caption 2", ...]
            },
            "campaign_settings": {
              "ad_placements": ["In-Feed", "Spark Ads"],
              "bidding_strategy": "Exact strategy",
              "bid_amount": "$0.50",
              "optimization_goals": "Conversions"
            },
            "creative_brief": {
              "video_script_outline": [
                {"timestamp": "0-3s", "content": "Exact content"},
                {"timestamp": "4-10s", "content": "Exact content"}
              ],
              "key_visuals": ["Visual 1", "Visual 2"],
              "text_overlays": ["Overlay 1", "Overlay 2"]
            }
          },
          ...
        }
        """
    )


def create_google_ads_campaign_task(context):
    """Task: Create Google Ads campaign"""
    return Task(
        description="""
        Create a complete Google Ads campaign for approved products:
        
        CRITICAL: Extract data from previous tasks:
        - Task 16 (Marketing Strategy): Use headline_variations, key_messages, target_audience
        - Task 15 (SEO): Use target_keywords for keyword strategy
        - Task 11 (Decision): Get list of approved products
        
        For EACH approved product, create EXACT campaign configuration:
        
        1. Campaign structure (EXACT values):
           - Search Campaign:
             * Name: "ProductName_Search_2024"
             * Objective: "Sales" or "Leads" (be specific)
             * Daily budget: EXACT amount (e.g., "$30/day")
             * Total budget: EXACT amount (e.g., "$900 for 30 days")
           - Shopping Campaign:
             * Name: "ProductName_Shopping_2024"
             * Objective: "Sales"
             * Daily budget: EXACT amount (e.g., "$20/day")
           - Display Campaign:
             * Name: "ProductName_Display_2024"
             * Objective: "Brand awareness and retargeting"
             * Daily budget: EXACT amount (e.g., "$10/day")
        
        2. Keyword strategy (EXACT keywords):
           - Primary keywords (high-intent, exact match): EXACT list (e.g., ["best phone stand", "adjustable phone stand cable"])
           - Secondary keywords (phrase match): EXACT list (e.g., ["phone stand for desk", "cable phone stand"])
           - Long-tail keywords (broad match modifier): EXACT list (e.g., ["affordable phone stand cable", "easy install phone stand"])
           - Negative keywords: EXACT list (e.g., ["free", "cheap", "used", "wholesale"])
           - Match types: SPECIFY for each (e.g., "Primary: Exact Match", "Secondary: Phrase Match")
        
        3. Ad copy creation (READY TO USE):
           - Search ad headlines: 15 EXACT headlines (max 30 characters each, ready to copy-paste)
           - Search ad descriptions: 4 EXACT descriptions (max 90 characters each, ready to copy-paste)
           - Responsive search ads: SPECIFIC headline/description combinations
           - Shopping ad title: EXACT title (max 150 characters)
           - Shopping ad description: EXACT description (max 5000 characters)
        
        4. Campaign settings (EXACT configuration):
           - Geographic targeting: EXACT countries/regions (e.g., "United States, Canada, United Kingdom, Australia")
           - Device targeting: EXACT settings (e.g., "Mobile: +20% bid adjustment, Desktop: -10% bid adjustment")
           - Schedule: EXACT schedule (e.g., "7 days/week, 8AM-10PM EST")
           - Bidding strategy: EXACT strategy (e.g., "Maximize Conversions with Target CPA: $5.00")
           - Conversion tracking: SPECIFIC events (e.g., "Purchase", "Add to Cart", "Sign Up")
        
        5. Landing page alignment:
           - Ad copy to landing page mapping: SPECIFIC (e.g., "Headline 'Premium Sound' → Landing page hero section")
           - Keyword consistency: EXACT keywords to use on landing page
           - Message continuity: SPECIFIC message flow (e.g., "Ad: '30-hour battery' → Landing: 'All-day power' section")
        
        IMPORTANT:
        - Be EXACT and ACTIONABLE - every setting should be ready to configure in Google Ads
        - Use REAL keywords from SEO task
        - Use REAL messaging from marketing strategy
        - For EACH approved product, create complete campaign
        - Return JSON format with all products
        
        Return complete Google Ads campaign plan in JSON format with EXACT configuration values.
        """,
        agent=create_google_ads_agent(),
        context=context,
        expected_output="""
        JSON object with Google Ads campaign for each approved product:
        {
          "Product Name": {
            "campaign_structure": {
              "search_campaign": {
                "name": "Exact campaign name",
                "objective": "Sales",
                "daily_budget": "$30",
                "total_budget": "$900"
              },
              "shopping_campaign": {
                "name": "Exact campaign name",
                "objective": "Sales",
                "daily_budget": "$20"
              },
              "display_campaign": {
                "name": "Exact campaign name",
                "objective": "Brand awareness",
                "daily_budget": "$10"
              }
            },
            "keyword_strategy": {
              "primary_keywords": ["Exact keyword 1", "Exact keyword 2"],
              "secondary_keywords": ["Keyword 1", ...],
              "long_tail_keywords": ["Long tail 1", ...],
              "negative_keywords": ["Negative 1", ...],
              "match_types": {
                "primary": "Exact Match",
                "secondary": "Phrase Match",
                "long_tail": "Broad Match Modifier"
              }
            },
            "ad_copy": {
              "search_headlines": ["Headline 1 (30 chars)", "Headline 2", ...],
              "search_descriptions": ["Description 1 (90 chars)", ...],
              "shopping_title": "Exact shopping title",
              "shopping_description": "Exact shopping description"
            },
            "campaign_settings": {
              "geographic_targeting": ["Country 1", "Country 2"],
              "device_targeting": "Exact device settings",
              "schedule": "Exact schedule",
              "bidding_strategy": "Exact bidding strategy",
              "conversion_tracking": ["Event 1", "Event 2"]
            }
          },
          ...
        }
        """
    )


def create_facebook_ads_campaign_task(context):
    """Task: Create Facebook & Instagram Ads campaign"""
    return Task(
        description="""
        Create a complete Facebook and Instagram advertising campaign:
        
        CRITICAL: Extract data from previous tasks:
        - Task 16 (Marketing Strategy): Use headline_variations, key_messages, target_audience
        - Task 11 (Decision): Get list of approved products
        
        For EACH approved product, create EXACT campaign configuration:
        
        1. Campaign structure (EXACT values):
           - Campaign name: "ProductName_FB_IG_2024"
           - Campaign objective: "Conversions" (be specific)
           - Ad sets: Create 3 EXACT ad sets:
             * Ad Set 1: "Website Visitors & Lookalikes"
               - Daily budget: EXACT amount (e.g., "$15/day")
               - Optimization: "Conversions (Purchase)"
               - Bid strategy: EXACT (e.g., "Lowest Cost" or "Cost Cap: $5.00")
             * Ad Set 2: "Interest Targeting"
               - Daily budget: EXACT amount (e.g., "$20/day")
               - Optimization: "Conversions (Purchase)"
             * Ad Set 3: "Retargeting"
               - Daily budget: EXACT amount (e.g., "$10/day")
               - Optimization: "Conversions (Purchase)"
           - Total budget: EXACT amount (e.g., "$1350 for 30 days")
           - Campaign duration: EXACT dates (e.g., "2024-02-01 to 2024-03-02")
        
        2. Audience targeting (EXACT settings):
           - Custom Audiences: SPECIFIC sources (e.g., "Website visitors last 30 days", "Email subscribers", "Facebook page engagers")
           - Lookalike Audiences: EXACT source and similarity (e.g., "Website purchasers, Top 1% similar, United States")
           - Interest targeting: EXACT interests (e.g., ["Electronics", "Home & Garden", "Tech Gadgets"])
           - Behavior targeting: EXACT behaviors (e.g., ["Online shoppers", "Mobile device users"])
           - Demographic targeting: EXACT demographics (e.g., "Age: 25-55, Gender: All, Education: College+")
           - Geographic targeting: EXACT locations (e.g., "United States, Canada, United Kingdom, Australia")
           - Exclusions: EXACT exclusions (e.g., "People who visited competitor sites", "People who already purchased")
        
        3. Ad creative strategy (READY TO USE):
           - Image ad concepts: 5 SPECIFIC concepts with EXACT descriptions:
             * Concept 1: SPECIFIC description, EXACT overlay text, EXACT CTA
             * Concept 2: ...
           - Video ad concepts: 5 SPECIFIC concepts with EXACT descriptions:
             * Concept 1: SPECIFIC description, EXACT length (e.g., "15 seconds"), EXACT overlay text
             * Concept 2: ...
           - Ad copy variations: 10 EXACT captions ready to use (max 125 characters for primary text)
           - Headline variations: 10 EXACT headlines (max 40 characters each)
           - Primary text variations: 5 EXACT primary texts (max 125 characters each)
        
        4. Campaign settings (EXACT configuration):
           - Ad placements: EXACT placements (e.g., ["Facebook Feed", "Instagram Feed", "Instagram Stories", "Facebook Marketplace"])
           - Budget optimization: EXACT strategy (e.g., "Campaign Budget Optimization: ON")
           - Bidding strategy: EXACT strategy per ad set (e.g., "Ad Set 1: Lowest Cost", "Ad Set 2: Cost Cap $5.00")
           - Conversion tracking: SPECIFIC events (e.g., "Purchase", "Add to Cart", "Initiate Checkout")
           - Facebook Pixel: SPECIFIC pixel events to track
        
        5. Creative specifications (EXACT requirements):
           - Image dimensions: EXACT sizes (e.g., "Facebook Feed: 1200x628px, Instagram Feed: 1080x1080px")
           - Image format: EXACT format (e.g., "JPG or PNG, max 30MB")
           - Video length: EXACT length (e.g., "15-30 seconds")
           - Video format: EXACT format (e.g., "MP4, H.264, max 4GB")
           - Text overlay guidelines: EXACT rules (e.g., "Max 20% of image, use bold font, white text with black outline")
           - Brand guidelines: SPECIFIC colors, fonts, logos to use
        
        IMPORTANT:
        - Be EXACT and ACTIONABLE - every setting should be ready to configure in Facebook Ads Manager
        - Use REAL messaging from marketing strategy
        - For EACH approved product, create complete campaign
        - Return JSON format with all products
        
        Return complete Facebook/Instagram campaign plan in JSON format with EXACT configuration values.
        """,
        agent=create_facebook_ads_agent(),
        context=context,
        expected_output="""
        JSON object with Facebook/Instagram campaign for each approved product:
        {
          "Product Name": {
            "campaign_objective": "Conversions",
            "campaign_structure": {
              "campaign_name": "Exact campaign name",
              "ad_sets": [
                {
                  "name": "Website Visitors & Lookalikes",
                  "daily_budget": "$15",
                  "optimization": "Conversions (Purchase)",
                  "bid_strategy": "Exact bid strategy"
                },
                {
                  "name": "Interest Targeting",
                  "daily_budget": "$20",
                  "optimization": "Conversions (Purchase)",
                  "bid_strategy": "Exact bid strategy"
                },
                {
                  "name": "Retargeting",
                  "daily_budget": "$10",
                  "optimization": "Conversions (Purchase)",
                  "bid_strategy": "Exact bid strategy"
                }
              ],
              "total_budget": "$1350",
              "duration_days": 30
            },
            "audience_targeting": {
              "custom_audiences": ["Exact audience 1", ...],
              "lookalike_audiences": ["Exact lookalike 1", ...],
              "interest_targeting": ["Exact interest 1", ...],
              "demographic_targeting": {
                "age": "25-55",
                "gender": "All",
                "education": "College+"
              },
              "geographic_targeting": ["Country 1", "Country 2"]
            },
            "ad_creative_strategy": {
              "image_ad_concepts": [
                {
                  "concept_name": "Exact concept name",
                  "description": "Exact description",
                  "overlay_text": "Exact overlay text",
                  "call_to_action": "Exact CTA"
                },
                ...
              ],
              "video_ad_concepts": [
                {
                  "concept_name": "Exact concept name",
                  "description": "Exact description",
                  "length": "15 seconds",
                  "overlay_text": "Exact overlay text"
                },
                ...
              ],
              "ad_copy_variations": ["Exact caption 1", "Exact caption 2", ...],
              "headline_variations": ["Exact headline 1", ...],
              "primary_text_variations": ["Exact primary text 1", ...]
            },
            "campaign_settings": {
              "ad_placements": ["Exact placement 1", ...],
              "bidding_strategy": "Exact bidding strategy",
              "optimization_goals": "Conversions (Purchase)",
              "conversion_tracking": ["Event 1", "Event 2"]
            },
            "creative_specifications": {
              "image_dimensions": "Exact dimensions",
              "video_length": "15-30 seconds",
              "text_overlay_guidelines": "Exact guidelines"
            }
          },
          ...
        }
        """
    )
