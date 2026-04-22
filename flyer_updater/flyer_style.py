STYLE=f"""
    <style>
        [data-testid="stChatMessage"],
        [data-testid="stChatMessage"] * {{
        color: #ffffff;
        }}
        .st-key-chat_container{{
            border: none;
            border-radius: 10px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        .st-key-input_container [class*="st-key-audio_file_upload"] > div > div:nth-child(2) {{
            height: 40px !important;
            min-height: 40px !important;
        }}
        .st-key-input_container{{
            color: #C9D0DA;
            border: none;
            border-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }}
        .st-key-selector_container label,
        .st-key-selector_container label p {{
            color: #D3AF37 !important;
            text-shadow: 0 0 1px rgba(255, 255, 255, 0.8);
        }}
        .st-key-page_container{{
            background: linear-gradient(to top, #012169, #00539B);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        }}
        .st-key-camera,.st-key-upload{{
            /* margin-top: -15px; */
            /* margin-bottom: -125px; */
            border-radius: 0px;
        }}
        .st-key-landing_page_container{{
            border-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            gap:0px;
        }}
        .st-key-header{{
            text-shadow:2px 2px 4px rgba(0,0,0,0.5);
            /* margin-bottom:-45px; */
        }}
        .st-key-top{{
            color: #ffffff;
            text-align: center;
            padding: 10px;
            margin-bottom:-20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
    </style>
"""
