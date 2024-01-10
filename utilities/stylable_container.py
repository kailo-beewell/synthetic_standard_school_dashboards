import streamlit as st

def stylable_container(key, css_styles):
    '''
    This is copied from streamlit-extras.
    Insert a container into your app which you can style using CSS.
    This is useful to style specific elements in your app.

    Args:
        key (str): The key associated with this container. This needs to be unique since all styles will be
            applied to the container with this key.
        css_styles (str | List[str]): The CSS styles to apply to the container elements.
            This can be a single CSS block or a list of CSS blocks.

    Returns:
        DeltaGenerator: A container object. Elements can be added to this container using either the 'with'
            notation or by calling methods directly on the returned object.
    '''
    if isinstance(css_styles, str):
        css_styles = [css_styles]

    # Remove unneeded spacing that is added by the style markdown:
    css_styles.append(
        '''
> div:first-child {
    margin-bottom: -1rem;
}
'''
    )

    style_text = '''
<style>
'''

    for style in css_styles:
        style_text += f'''

div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.{key}) {style}

'''

    style_text += f'''
    </style>

<span class="{key}"></span>
'''

    container = st.container()
    container.markdown(style_text, unsafe_allow_html=True)
    return container


def header_container(key, text, colour):
    '''
    Create a stylised container for the About page to container a header

    Args:
        key (str): Key for container type
        text (str): Header text
        colour (str): HEX colour code for background of container
    '''
    st.text('')
    st.text('')
    with stylable_container(
            key=key,
            css_styles=f'''
                {{
                    background-color: {colour};
                    border-radius: 0.5rem;
                    padding: 0px
                }}
                ''',
        ):
            # Add header in markdown so can add some blank space to start of line
            st.markdown(f'<h2>&nbsp&nbsp{text}</hr>', unsafe_allow_html=True)
            st.text('')