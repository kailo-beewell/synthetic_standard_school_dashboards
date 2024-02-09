'''
Generic function to produce stylised containers and then specific function
for producing the stylised header containers used on the About page
'''
import streamlit as st
from utilities.page_setup import blank_lines


def stylable_container(key, css_styles):
    '''
    This function is copied from streamlit-extras. It creates inserts a
    container in the app that we are able to style using CSS.

    Parameters
    ----------
    key : str
        The unique key associated with container
    css_styles : str | list[str]
        The CSS styles to apply to the container elements. This can be a single
        CSS block or a list of CSS blocks.

    Returns:
    container
        A container object. Elements can be added to this container using
        either the 'with' notation or by calling methods directly on the
        returned object.
    '''
    # If CSS style provided is a string, insert it into a list
    if isinstance(css_styles, str):
        css_styles = [css_styles]

    # Remove unneeded spacing that is added by the style markdown:
    css_styles.append('''
> div:first-child {
    margin-bottom: -1rem;
}
''')

    # Use provided CSS to write the full CSS to style the container
    style_text = '<style>'
    for style in css_styles:
        style_text += f'''
div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown
> div[data-testid="stMarkdownContainer"] > p > span.{key}) {style}'''
    style_text += f'''
</style>
<span class="{key}"></span>'''

    # Produce the container and apply style
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
    blank_lines(2)
    with stylable_container(
            key=key,
            css_styles=f'''
{{
    background-color: {colour};
    border-radius: 0.5rem;
    padding: 0px
}}''',):
        # Add header in markdown so can add some blank space to start of line
        st.markdown(f'<h2>&nbsp&nbsp{text}</hr>', unsafe_allow_html=True)
        blank_lines(1)
