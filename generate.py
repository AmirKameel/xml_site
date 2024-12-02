import streamlit as st
import openai
import base64

# Fixed metadata for XML generation
fixed_metadata = {
    'site_link': 'https://example.com',
    'language': 'en-US',
    'generator': 'Streamlit WordPress Site Generator',
    'wxr_version': '1.2',
    'base_site_url': 'https://example.com',
    'base_blog_url': 'https://example.com'
}

def generate_xml(site_title, site_description, site_category, elementor_data):
    xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
     xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:wfw="http://wellformedweb.org/CommentAPI/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>{site_title}</title>
    <link>{fixed_metadata['site_link']}</link>
    <description>{site_description}</description>
    
    <language>{fixed_metadata['language']}</language>
    <generator>{fixed_metadata['generator']}</generator>
    <wp:wxr_version>{fixed_metadata['wxr_version']}</wp:wxr_version>
    <wp:base_site_url>{fixed_metadata['base_site_url']}</wp:base_site_url>
    <wp:base_blog_url>{fixed_metadata['base_blog_url']}</wp:base_blog_url>

    <item>
        <title><![CDATA[{site_title}]]></title>
        <link>https://webelly.com/sample-page</link>
      
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://webelly.com/sample-page</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>1001</wp:post_id>

        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[sample-page]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <category><![CDATA[{site_category}]]></category>
        {elementor_data}
    </item>
</channel>
</rss>
"""
    return xml_content

def create_download_link(content, filename):
    """
    Create a base64 encoded download link for the file
    """
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:application/xml;base64,{b64}" download="{filename}">Download XML File</a>'

def chat_with_model(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            max_tokens=16383
        )
        
        # Get the model's response
        model_response = response.choices[0].message.content
        
        # Add model's response to messages
        messages.append({"role": "assistant", "content": model_response})
        
        return model_response, messages
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, messages

def main():
    # Set page configuration
    st.set_page_config(page_title="WordPress Website Generator", page_icon="🌐")
    
    # Initialize OpenAI API key
    openai.api_key = st.secrets.get("OPENAI_API_KEY")
    
    # Title
    st.title("WordPress Website Generator with Elementor")
    
    # Ensure clean state management
    if 'stage' not in st.session_state:
        st.session_state.stage = 'input'

    # Site Information Input Stage
    if st.session_state.stage == 'input':
        st.subheader("Site Information")
        site_title = st.text_input("Website Title")
        site_description = st.text_area("Website Description")
        site_category = st.text_input("Website Category")
        design_preferences = st.text_area("Design Preferences (optional)")
        
        if st.button("Start Website Generation"):
            # Validate inputs
            if not site_title or not site_description or not site_category:
                st.warning("Please fill in all required fields.")
                return

            # Store site information
            st.session_state.site_title = site_title
            st.session_state.site_description = site_description
            st.session_state.site_category = site_category
            st.session_state.design_preferences = design_preferences
            
            # Detailed initial prompt for the AI
            initial_prompt = f"""You are an expert WordPress website designer using Elementor. I want to create a professional website with the following details:

Website Title: {site_title}
Website Description: {site_description}
Website Category: {site_category}
Design Preferences: {design_preferences}
"""
            
            # Initialize messages with system and initial prompt
            st.session_state.messages = [
                {"role": "system", "content": """you are an expert xml wordpress developer with elementor , you are tasked to create xml file to be valid to upload in wordpress with elementor tags , elementor data tag should enclude 5 sections , like hero section , about us section , services section ,  and contact us section  so make it over 8000 token about 100k chars output if needed
  so first ask the user about his website name and catogery and description and if he wanted some addetional details like if he want it modern , professional and so on , but on that , you first act like a web desinger make reccomandtions From color schemes to layout suggestions , suggest everything in each section and after the user approve your suggested desing return all the desing in a valid xml file
  here is some images you can use , for about us : "https://wp-ai.webmeccano.me/wp-content/uploads/2024/07/slide-3-300x225.jpg"
  for background image : "https://wp-ai.webmeccano.me/wp-content/uploads/2024/07/photo-1516321318423-f06f85e504b3-scaled.jpg"
  after user aprove when generating the elementor data "just return full <wp:postmeta> tag without any text explantion or any strings or '''xml , just the code"
  be sure you make some padding between each section to looks well
The website should include the following sections:
Hero Section:
Fullscreen background image.
A centered heading with a catchy tagline and a subheading.
A call-to-action button with a link.
About Us Section:
Two-column layout.
Left column: Image with a border or shadow effect.
Right column: Heading, a brief description, and a second call-to-action button.
Services Section:
Three equal-width columns, each featuring an icon, a heading, and a brief description.
Portfolio/Projects Section:
A gallery or grid layout with placeholder images and titles for showcasing projects.
Contact Section
here is elementor data example for a hero section :
"{"id":"heroSection","elType":"container","settings":{"layout":"full_width","min_height":{"unit":"vh","size":100,"sizes":[]},"background_background":"classic","background_image":{"url":"https://wp-ai.webmeccano.me/wp-content/uploads/2024/07/photo-1516321318423-f06f85e504b3-scaled.jpg"},"background_position":"center center","background_size":"cover"},"elements":[{"id":"heroContainer","elType":"container","settings":{"content_width":"boxed","flex_direction":"column","align_items":"center","padding":{"unit":"px","top":"60","right":"20","bottom":"60","left":"20","isLinked":false}},"elements":[{"id":"heroHeading","elType":"widget","settings":{"title":"Welcome to WebMeccano","align":"center","title_color":"#1E3A8A","typography_typography":"custom","typography_font_family":"Montserrat","typography_font_size":{"unit":"px","size":50,"sizes":[]},"typography_font_weight":"700"},"elements":[],"widgetType":"heading"},{"id":"heroSubHeading","elType":"widget","settings":{"title":"Innovative AI Solutions for Web Development","align":"center","title_color":"#22D3EE","typography_typography":"custom","typography_font_family":"Montserrat","typography_font_size":{"unit":"px","size":30,"sizes":[]},"typography_font_weight":"500"},"elements":[],"widgetType":"heading"}],"isInner":true}],"isInner":false}, complete other sections like that"
here is example too for contact :
        {"id":"contactUsSection","elType":"container","settings":{"flex_direction":"row","content_width":"full","min_height":{"unit":"px","size":833,"sizes":[]},"background_background":"classic","background_color":"#FFFFFF"},"elements":[{"id":"contactText","elType":"container","settings":{"content_width":"full","width":{"unit":"%","size":"50"},"flex_justify_content":"center","background_background":"classic","padding":{"unit":"%","top":"0","right":"6","bottom":"0","left":"6","isLinked":false},"background_color":"#F3F5F8"},"elements":[{"id":"contactHeading","elType":"widget","settings":{"title":"Contact Us","header_size":"h1","align":"left","title_color":"#1C244B","typography_typography":"custom","typography_font_family":"Poppins","typography_font_size":{"unit":"px","size":65,"sizes":[]},"typography_font_weight":"600"},"elements":[],"widgetType":"heading"},{"id":"contactSubHeading","elType":"widget","settings":{"title":"We would love to speak with you.<br>Feel free to reach out using the below details.","header_size":"p","title_color":"#1C244B","typography_typography":"custom","typography_font_family":"Poppins","typography_font_size":{"unit":"px","size":22,"sizes":[]},"typography_font_weight":"300"},"elements":[],"widgetType":"heading"}],"isInner":true},{"id":"contactForm","elType":"container","settings":{"content_width":"full","width":{"unit":"%","size":"50"},"flex_justify_content":"center","padding":{"unit":"%","top":"0","right":"6","bottom":"0","left":"6","isLinked":false},"flex_gap":{"unit":"px","size":20,"sizes":[]},"background_color":"#F3F5F8"},"elements":[{"id":"contactFormWidget","elType":"widget","settings":{"form_name":"Contact Form","form_fields":[{"custom_id":"name","field_label":"Your Name","placeholder":"Your Name*","_id":"e073133","width":"50","required":"true"},{"custom_id":"field_b743cd7","required":"true","field_label":"Last Name","placeholder":"Last Name*","width":"50","_id":"b743cd7"},{"custom_id":"field_6c180a9","field_type":"tel","required":"true","field_label":"Phone Number","placeholder":"Phone Number*","width":"50","_id":"6c180a9"},{"custom_id":"email","field_type":"email","required":"true","field_label":"Email","placeholder":"Email*","_id":"cd2e872","width":"50"},{"custom_id":"message","field_type":"textarea","field_label":"Message","placeholder":"Message","_id":"6e37168"}],"step_next_label":"Next","step_previous_label":"Previous","button_text":"Submit","email_content":"[all-fields]","email_content_2":"[all-fields]","success_message":"The form was sent successfully.","error_message":"An error occurred.","required_field_message":"This field is required.","html_spacing":{"unit":"px","size":"41","sizes":[]},"button_align":"start","column_gap":{"unit":"px","size":"30","sizes":[]},"row_gap":{"unit":"px","size":"20","sizes":[]},"field_text_color":"#324A6D","field_border_color":"#C8D5DC","field_border_width":{"unit":"px","top":"1","right":"1","bottom":"1","left":"1","isLinked":"1"},"button_text_color":"#FFFFFF","button_border_color":"#467FF7","button_background_hover_color":"#02010100","button_hover_color":"#467FF7","button_hover_border_color":"#467FF7","button_border_radius":{"unit":"px","top":"50","right":"50","bottom":"50","left":"50","isLinked":"1"},"button_text_padding":{"unit":"%","top":"3","right":"13","bottom":"3","left":"13","isLinked":""},"success_message_color":"#467FF7","error_message_color":"#324A6D","inline_message_color":"#324A6D","label_color":"#324A6D"},"elements":[],"widgetType":"form"}],"isInner":true}],"isInner":false}
so make other sections like that and donot forget to return them under this tag
<wp:postmeta>
    <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
    <wp:meta_value> with close the tags
"""},
                {"role": "user", "content": initial_prompt}
            ]
            
            # Change stage to chat
            st.session_state.stage = 'chat'
            
            # Generate initial response
            response, updated_messages = chat_with_model(initial_prompt, st.session_state.messages)
            st.session_state.messages = updated_messages

            # Force rerun to show chat interface
            st.rerun()

    # Chat Interface Stage
    if st.session_state.stage == 'chat':
        # Sidebar for site info display
        with st.sidebar:
            st.write("### Site Details")
            st.write(f"**Title:** {st.session_state.site_title}")
            st.write(f"**Category:** {st.session_state.site_category}")
            st.write(f"**Description:** {st.session_state.site_description}")

        # Display chat messages
        for message in st.session_state.messages:
            if message['role'] not in ['system']:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
        
        # Chat input
        if prompt := st.chat_input("Discuss the design or request modifications"):
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.spinner('Generating response...'):
                response, updated_messages = chat_with_model(prompt, st.session_state.messages)
            
            # Update messages
            st.session_state.messages = updated_messages
            
            # Display assistant response
            if response:
                with st.chat_message("assistant"):
                    st.markdown(response)
                

                    xml_content = generate_xml(
                                st.session_state.site_title, 
                                st.session_state.site_description, 
                                st.session_state.site_category, 
                                response
                            )
                            
                            # Create download link
                    st.download_button(
            label="Download Full XML",
            data=xml_content,
            file_name="site.xml",
            mime="application/xml",
        )
                        


if __name__ == "__main__":
    main()
