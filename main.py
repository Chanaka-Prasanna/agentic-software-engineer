import streamlit as st
from agent.graph import agent
import os

st.title("🤖 AI Software Engineer")
st.write("Describe the web application you want to build, and I'll generate it for you!")

# User input
user_prompt = st.text_area(
    "Enter your project description:",
    placeholder="e.g., Create a currency converter web application",
    height=150
)

# Generate button
if st.button("Generate Project", type="primary"):
    if user_prompt.strip():
        # Create a status container for streaming updates
        status_container = st.container()
        
        with status_container:
            with st.spinner("🔧 Planning and building your project..."):
                try:
                    # Invoke the agent
                    result = agent.invoke(
                        {"user_prompt": user_prompt},
                        {"recursion_limit": 100}
                    )
                    
                    # Show success message
                    st.success("✅ Project generated successfully!")
                    
                    # Get the absolute path to generated_project
                    project_path = os.path.abspath("agent/generated_project")
                    
                    # Display completion message
                    st.info(f"""
                    ### 🎉 Your project is ready!
                    
                    **Location:** `{project_path}`
                    
                    Check the **agent/generated_project** directory in your workspace for all generated files.
                    """)
                    
                    # Optionally show the result details in an expander
                    with st.expander("📋 View Generation Details"):
                        st.json(result)
                        
                except Exception as e:
                    st.error(f"❌ Error during generation: {str(e)}")
    else:
        st.warning("⚠️ Please enter a project description first.")