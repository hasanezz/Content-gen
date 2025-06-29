import streamlit as st
import openai
import json
from typing import List, Dict
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Iraqi Remittance Segments - Social Media Reaction Simulator",
    page_icon="📱",
    layout="wide",
)

# Define comprehensive audience segments based on your document
AUDIENCE_SEGMENTS = {
    "Iraqi Students Abroad": {
        "description": "Iraqi students studying abroad who receive financial support (remittances) from family in Iraq",
        "subsegments": [
            "Undergraduate Students",
            "Master's Students",
            "PhD/Research Scholars",
            "Working Students",
            "First-Year Students",
            "Final-Year Students",
        ],
        "age_range": "17-35",
        "motivations": [
            "Family fulfilling educational dreams",
            "Tuition and living expenses",
            "Emergency needs abroad",
            "Currency arbitrage benefits",
        ],
        "traits": [
            "aspirational",
            "family-oriented",
            "budget-conscious",
            "technophile",
            "security-oriented",
        ],
        "key_concerns": [
            "tuition costs",
            "living expenses",
            "family support",
            "academic success",
            "fast transfers",
        ],
        "platforms": ["Western Union", "Remitly", "Wise", "WorldRemit", "Revolut"],
        "keywords": [
            "Iraqi student",
            "tuition remittance",
            "send money to student",
            "study abroad support",
        ],
    },
    "Iraqi Workers Abroad": {
        "description": "Iraqi workers abroad sending remittances back home to support families and communities",
        "subsegments": [
            "Construction Workers",
            "Healthcare Workers",
            "Domestic Workers",
            "Tech Workers",
            "Service Industry",
        ],
        "age_range": "20-60",
        "motivations": [
            "Fulfilling family obligations",
            "Building home/investments in Iraq",
            "Supporting medical care",
            "Social status and pride",
        ],
        "traits": [
            "family-oriented",
            "sacrificial",
            "community-led",
            "resilient",
            "goal-oriented",
            "traditional",
        ],
        "key_concerns": [
            "family support",
            "reliable transfers",
            "low fees",
            "fast delivery",
            "privacy",
        ],
        "platforms": [
            "Western Union",
            "Remitly",
            "Ria",
            "Tahweel",
            "Al Ansari",
            "Hawala",
        ],
        "keywords": [
            "send money to Iraq",
            "Iraqi remittance",
            "support family Iraq",
            "hawala Iraq",
            "low cost transfer",
        ],
    },
    "Iraqi Diaspora Community": {
        "description": "Long-term Iraqi diaspora maintaining cultural and financial ties with home country",
        "subsegments": [
            "Long-term Settled Expats",
            "Refugee Diaspora",
            "Business Professionals",
            "Second-generation Diaspora",
        ],
        "age_range": "25-65+",
        "motivations": [
            "Preserving cultural ties",
            "Supporting community events",
            "Property investments",
            "Emergency family support",
        ],
        "traits": [
            "aspirational",
            "family-oriented",
            "technophile",
            "security-oriented",
            "culturally rooted",
            "community-minded",
        ],
        "key_concerns": [
            "cultural preservation",
            "family emergencies",
            "investment opportunities",
            "trusted services",
        ],
        "platforms": [
            "Western Union",
            "MoneyGram",
            "Wise",
            "Traditional hawala networks",
        ],
        "keywords": [
            "Iraqi diaspora",
            "Iraqi community abroad",
            "support family Iraq",
            "cultural remittance",
        ],
    },
    "Freelancers & Remote Workers": {
        "description": "Digitally connected individuals in Iraq earning from international clients and managing cross-border payments",
        "subsegments": [
            "Platform Freelancers",
            "Remote Employees",
            "Creative Professionals",
            "Developers & IT",
            "Crypto-earning Freelancers",
        ],
        "age_range": "20-45",
        "motivations": [
            "Income access and conversion",
            "Business investment",
            "Global market access",
            "Equipment upgrades",
        ],
        "traits": [
            "entrepreneurial",
            "tech-savvy",
            "independent",
            "global-minded",
            "resilient",
            "status-seeking",
        ],
        "key_concerns": [
            "fast USD access",
            "low conversion fees",
            "crypto options",
            "reliable platforms",
        ],
        "platforms": [
            "Payoneer",
            "Wise",
            "Crypto wallets",
            "Upwork payments",
            "Freelancer platforms",
        ],
        "keywords": [
            "freelancer Iraq",
            "Payoneer Iraq",
            "receive USD Iraq",
            "Upwork withdrawal",
            "crypto Iraq",
        ],
    },
    "Business Owners & Importers": {
        "description": "Iraqi business owners and import/export operators sending money abroad for business operations",
        "subsegments": [
            "Small Local Businesses",
            "Medium Enterprises",
            "Import/Export Firms",
            "Online Sellers",
            "Exporters",
        ],
        "age_range": "30-60+",
        "motivations": [
            "Supplier payments",
            "Business expansion",
            "Supply chain operations",
            "International partnerships",
        ],
        "traits": [
            "entrepreneurial",
            "efficiency-focused",
            "relationship-driven",
            "security-conscious",
            "growth-oriented",
        ],
        "key_concerns": [
            "business continuity",
            "supplier relationships",
            "compliance",
            "cost efficiency",
        ],
        "platforms": [
            "Commercial banking",
            "Business wire transfers",
            "Trade finance platforms",
        ],
        "keywords": [
            "business payments Iraq",
            "international suppliers",
            "import export Iraq",
            "commercial transfers",
        ],
    },
    "Digital Entrepreneurs": {
        "description": "Iraqi entrepreneurs running online stores, digital services, or e-commerce platforms",
        "subsegments": [
            "Online Retailers",
            "Digital Service Providers",
            "Export-focused Sellers",
            "Dropshippers",
            "Social Media Sellers",
        ],
        "age_range": "20-45",
        "motivations": [
            "Business growth",
            "Market expansion",
            "Financial efficiency",
            "International reach",
        ],
        "traits": [
            "ambitious",
            "tech-savvy",
            "risk-tolerant",
            "customer-focused",
            "adaptable",
            "community-oriented",
        ],
        "key_concerns": [
            "payment processing",
            "international sales",
            "digital marketing",
            "platform fees",
        ],
        "platforms": [
            "Digital wallets",
            "E-commerce platforms",
            "Online banking",
            "Social media payments",
        ],
        "keywords": [
            "e-commerce Iraq",
            "online business Iraq",
            "digital payments Iraq",
            "Iraqi entrepreneurs",
        ],
    },
}


def analyze_segment_reaction(segment_name, segment_info, content, api_key):
    """Analyze how a specific segment would react to content"""

    prompt = f"""
    You are an expert in social media marketing and audience analysis for Iraqi remittance segments. Analyze how the following audience segment would react to a social media post.

    AUDIENCE SEGMENT: {segment_name}
    Description: {segment_info['description']}
    Age Range: {segment_info['age_range']}
    Subsegments: {', '.join(segment_info['subsegments'])}
    Key Motivations: {', '.join(segment_info['motivations'])}
    Key Traits: {', '.join(segment_info['traits'])}
    Main Concerns: {', '.join(segment_info['key_concerns'])}
    Preferred Platforms: {', '.join(segment_info['platforms'])}

    SOCIAL MEDIA CONTENT TO ANALYZE:
    "{content}"

    Please provide a detailed analysis in the following format:

    ENGAGEMENT LEVEL: [High/Medium/Low]
    EMOTIONAL RESPONSE: [Positive/Neutral/Negative/Mixed]
    
    REACTION ANALYSIS:
    [3-4 sentences explaining how this segment would likely react to the content, considering their motivations and concerns]
    
    KEY TRIGGERS:
    [List 3-4 specific elements that would trigger positive or negative responses for this segment]
    
    SEGMENT-SPECIFIC INSIGHTS:
    [2-3 insights about why this particular Iraqi segment would react this way, considering their cultural and financial context]
    
    IMPROVEMENT SUGGESTIONS:
    [3-4 specific suggestions to make the content more engaging for this segment]
    """

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def enhance_content_for_segments(original_content, selected_segments, api_key):
    """Enhance content for selected segments"""

    segments_info = ""
    for segment in selected_segments:
        info = AUDIENCE_SEGMENTS[segment]
        segments_info += f"\n{segment}:\n- Description: {info['description']}\n- Motivations: {', '.join(info['motivations'][:3])}\n- Key Concerns: {', '.join(info['key_concerns'][:3])}\n"

    prompt = f"""
    You are a social media content strategist specializing in Iraqi remittance and financial services. Enhance the following content to better appeal to these Iraqi segments:

    ORIGINAL CONTENT:
    "{original_content}"

    TARGET SEGMENTS:
    {segments_info}

    Consider the cultural context of Iraqi communities, remittance behaviors, and financial needs when enhancing the content.

    Please provide:

    ENHANCED CONTENT:
    [Improved version that appeals to the target segments, incorporating cultural nuances and specific pain points]

    ENHANCEMENT RATIONALE:
    [Explain specific changes made and how they address each segment's motivations and concerns]

    IRAQI ARABIC HOOKS:
    [3-4 short, catchy phrases in Iraqi Arabic dialect that would resonate with these segments]

    PLATFORM-SPECIFIC ADAPTATIONS:
    [Brief suggestions for how to adapt this content for WhatsApp, Instagram, Facebook, and Telegram]
    """

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def generate_iraqi_arabic_content(english_content, segment_name, api_key):
    """Generate Iraqi Arabic version of content"""

    segment_info = AUDIENCE_SEGMENTS[segment_name]

    prompt = f"""
    You are a native Iraqi Arabic speaker and social media expert specializing in remittance services. Create an Iraqi Arabic version of this content for {segment_name}.

    ENGLISH CONTENT:
    "{english_content}"

    TARGET SEGMENT: {segment_name}
    Description: {segment_info['description']}
    Key Motivations: {', '.join(segment_info['motivations'][:3])}
    Key Concerns: {', '.join(segment_info['key_concerns'][:3])}

    Consider the cultural context, family values, and specific financial behaviors of this Iraqi segment.

    Please provide:

    IRAQI ARABIC CONTENT:
    [Content in Iraqi Arabic dialect that authentically resonates with this segment's values and concerns]

    CULTURAL ADAPTATION NOTES:
    [Explain specific cultural elements incorporated and why they're important for this audience]

    EMOTIONAL TRIGGERS:
    [Identify 2-3 emotional appeals that work specifically for Iraqi culture and this segment]

    ENGAGEMENT TIPS:
    [Specific tips for using this content effectively with Iraqi audiences on social media]
    """

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    st.title("📱 Iraqi Remittance Segments - Social Media Reaction Simulator")
    st.markdown(
        "**Analyze how different Iraqi remittance segments react to your social media content**"
    )

    # Sidebar for API key and segment info
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to use the analyzer",
        )

        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("Please enter your OpenAI API key")

        st.header("📊 Iraqi Segments Overview")
        st.write(f"**Total Segments:** {len(AUDIENCE_SEGMENTS)}")

        for name, info in AUDIENCE_SEGMENTS.items():
            with st.expander(f"{name} ({info['age_range']})"):
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Subsegments:** {', '.join(info['subsegments'][:3])}...")
                st.write(
                    f"**Key Motivations:** {', '.join(info['motivations'][:2])}..."
                )
                st.write(
                    f"**Preferred Platforms:** {', '.join(info['platforms'][:3])}..."
                )

    # Main interface
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Content Input")

        # Sample content suggestions based on Iraqi context
        sample_posts = [
            "أرسل فلوس لأهلك بالعراق بسرعة وأمان! رسوم قليلة للطلاب. Send money home instantly! 🇮🇶💙",
            "Support your family back home while building your future abroad. Fast, secure, affordable. 🏠❤️",
            "من العراق للعالم - نربط المسافات بكل حوالة. From Iraq to the world - bridging distances. 🌍",
            "Your success abroad means everything to family back home. Quick remittances for Iraqis worldwide. 🎓",
            "Pay suppliers instantly. Grow your business. Iraq to global markets made simple. 💼🚀",
            "Freelancers - get paid faster from international clients. USD to IQD in minutes. 💻💰",
        ]

        st.subheader("💡 Sample Posts")
        selected_sample = st.selectbox(
            "Choose a sample post or write your own:", ["Custom"] + sample_posts
        )

        # Content input
        if selected_sample == "Custom":
            content_input = st.text_area(
                "Enter your social media post content:",
                placeholder="Write your social media post here...",
                height=150,
            )
        else:
            content_input = st.text_area(
                "Enter your social media post content:",
                value=selected_sample,
                height=150,
            )

        # Segment selection
        st.subheader("🎯 Select Iraqi Segments")
        selected_segments = st.multiselect(
            "Choose segments to analyze:",
            options=list(AUDIENCE_SEGMENTS.keys()),
            default=["Iraqi Students Abroad", "Iraqi Workers Abroad"],
            help="Select multiple segments to compare reactions across different Iraqi communities",
        )

        # Analysis type
        st.subheader("🔍 Analysis Type")
        analysis_type = st.radio(
            "Choose analysis type:",
            ["Reaction Analysis", "Content Enhancement", "Iraqi Arabic Adaptation"],
            help="Select what type of analysis you want to perform",
        )

        analyze_button = st.button(
            "🚀 Analyze Content",
            type="primary",
            disabled=not (api_key and content_input and selected_segments),
        )

    with col2:
        st.header("📊 Analysis Results")

        if not api_key:
            st.info(
                "👈 Please enter your OpenAI API key in the sidebar to start analyzing"
            )
        elif not content_input:
            st.info("👈 Please enter some content to analyze")
        elif not selected_segments:
            st.info("👈 Please select at least one Iraqi segment")
        elif analyze_button:

            if analysis_type == "Reaction Analysis":
                # Create tabs for each segment
                if len(selected_segments) > 1:
                    tabs = st.tabs(selected_segments)

                    for i, segment in enumerate(selected_segments):
                        with tabs[i]:
                            st.subheader(f"👥 {segment}")

                            # Show segment overview
                            segment_info = AUDIENCE_SEGMENTS[segment]
                            with st.expander("📋 Segment Details"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.write(f"**Age:** {segment_info['age_range']}")
                                    st.write(f"**Main Motivations:**")
                                    for motivation in segment_info["motivations"][:3]:
                                        st.write(f"• {motivation}")
                                with col_b:
                                    st.write(f"**Key Platforms:**")
                                    for platform in segment_info["platforms"][:3]:
                                        st.write(f"• {platform}")
                                    st.write(
                                        f"**Top Keywords:** {', '.join(segment_info['keywords'][:2])}"
                                    )

                            with st.spinner(f"Analyzing {segment} reaction..."):
                                result = analyze_segment_reaction(
                                    segment,
                                    AUDIENCE_SEGMENTS[segment],
                                    content_input,
                                    api_key,
                                )

                                if result.startswith("Error:"):
                                    st.error(result)
                                else:
                                    st.write(result)
                else:
                    # Single segment analysis
                    segment = selected_segments[0]
                    st.subheader(f"👥 {segment}")

                    # Show segment overview
                    segment_info = AUDIENCE_SEGMENTS[segment]
                    with st.expander("📋 Segment Details"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Age:** {segment_info['age_range']}")
                            st.write(f"**Description:** {segment_info['description']}")
                        with col_b:
                            st.write(
                                f"**Subsegments:** {', '.join(segment_info['subsegments'][:3])}"
                            )
                            st.write(
                                f"**Key Platforms:** {', '.join(segment_info['platforms'][:3])}"
                            )

                    with st.spinner(f"Analyzing {segment} reaction..."):
                        result = analyze_segment_reaction(
                            segment, AUDIENCE_SEGMENTS[segment], content_input, api_key
                        )

                        if result.startswith("Error:"):
                            st.error(result)
                        else:
                            st.write(result)

            elif analysis_type == "Content Enhancement":
                st.subheader("✨ Enhanced Content for Iraqi Segments")

                with st.spinner("Enhancing content for selected Iraqi segments..."):
                    result = enhance_content_for_segments(
                        content_input, selected_segments, api_key
                    )

                    if result.startswith("Error:"):
                        st.error(result)
                    else:
                        st.write(result)

            elif analysis_type == "Iraqi Arabic Adaptation":
                if len(selected_segments) > 1:
                    tabs = st.tabs(selected_segments)

                    for i, segment in enumerate(selected_segments):
                        with tabs[i]:
                            st.subheader(f"🔤 Arabic Version for {segment}")

                            with st.spinner(
                                f"Creating Iraqi Arabic version for {segment}..."
                            ):
                                result = generate_iraqi_arabic_content(
                                    content_input, segment, api_key
                                )

                                if result.startswith("Error:"):
                                    st.error(result)
                                else:
                                    st.write(result)
                else:
                    segment = selected_segments[0]
                    st.subheader(f"🔤 Arabic Version for {segment}")

                    with st.spinner(f"Creating Iraqi Arabic version for {segment}..."):
                        result = generate_iraqi_arabic_content(
                            content_input, segment, api_key
                        )

                        if result.startswith("Error:"):
                            st.error(result)
                        else:
                            st.write(result)

    # Segment comparison table
    if selected_segments and len(selected_segments) > 1:
        st.header("🔍 Iraqi Segments Comparison")

        comparison_data = []
        for segment in selected_segments:
            segment_info = AUDIENCE_SEGMENTS[segment]
            comparison_data.append(
                {
                    "Segment": segment,
                    "Age Range": segment_info["age_range"],
                    "Primary Motivation": (
                        segment_info["motivations"][0]
                        if segment_info["motivations"]
                        else "N/A"
                    ),
                    "Key Concern": (
                        segment_info["key_concerns"][0]
                        if segment_info["key_concerns"]
                        else "N/A"
                    ),
                    "Top Platform": (
                        segment_info["platforms"][0]
                        if segment_info["platforms"]
                        else "N/A"
                    ),
                    "Main Keywords": (
                        ", ".join(segment_info["keywords"][:2])
                        if segment_info["keywords"]
                        else "N/A"
                    ),
                }
            )

        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)

    # Enhanced tips section for Iraqi context
    with st.expander("💡 Iraqi Remittance Marketing Tips"):
        st.markdown(
            """
        ### Segment-Specific Strategy:
        
        **🎓 Iraqi Students Abroad**
        - Focus on family emotional connection and educational dreams
        - Highlight fast transfers for tuition deadlines
        - Use mix of Arabic and English to show cultural bridge
        - Emphasize security and parental peace of mind
        
        **👷 Iraqi Workers Abroad**
        - Stress reliability and family obligation fulfillment
        - Show impact on family back home (medical care, education)
        - Use traditional values and community pride messaging
        - Highlight low fees and delivery confirmation
        
        **🏠 Iraqi Diaspora Community**
        - Focus on cultural preservation and community events
        - Emphasize long-term relationships and trust
        - Show support for cultural institutions and traditions
        - Use community testimonials and success stories
        
        **💻 Freelancers & Remote Workers**
        - Highlight speed of USD access and conversion
        - Focus on business growth and global opportunities
        - Emphasize modern, tech-forward solutions
        - Show integration with freelance platforms
        
        **🏢 Business Owners & Importers**
        - Stress efficiency and business continuity
        - Focus on supplier relationships and growth
        - Highlight compliance and security features
        - Show cost savings and time benefits
        
        **🛒 Digital Entrepreneurs**
        - Focus on scaling online business and market access
        - Highlight payment processing and international sales
        - Emphasize modern solutions for modern businesses
        - Show integration with e-commerce platforms
        
        ### Cultural Considerations:
        - **Family Values**: Always emphasize family support and connection
        - **Trust**: Use testimonials from Iraqi community members
        - **Religious Sensitivity**: Ensure halal/Islamic compliance messaging
        - **Language**: Mix Arabic phrases with English for authentic feel
        - **Visuals**: Use Iraqi flag colors, cultural symbols, family imagery
        - **Timing**: Consider Iraqi holidays, Ramadan, and cultural events
        """
        )


if __name__ == "__main__":
    main()
