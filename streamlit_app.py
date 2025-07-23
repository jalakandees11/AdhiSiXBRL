import streamlit as st
    from lxml import etree
    import pandas as pd

    st.title("Simple XBRL File Explorer (Cloud)")

    uploaded_file = st.file_uploader("Upload your XBRL (.xbrl) or XML file:", type=["xbrl", "xml"])

    if uploaded_file is not None:
        try:
            tree = etree.parse(uploaded_file)
            root = tree.getroot()

            facts = []
            for elem in root.iter():
                if 'contextRef' in elem.attrib:
                    tag = elem.tag.split('}')[-1]
                    ns = elem.tag.split('}')[0][1:] if '}' in elem.tag else ""
                    context = elem.attrib['contextRef']
                    value = elem.text
                    facts.append({
                        "Namespace": ns,
                        "Tag": tag,
                        "ContextRef": context,
                        "Value": value
                    })
            if facts:
                df = pd.DataFrame(facts)
                st.dataframe(df)
            else:
                st.info("No 'contextRef' facts found in the uploaded file.")

        except Exception as e:
            st.error(f"Error parsing file: {e}")
