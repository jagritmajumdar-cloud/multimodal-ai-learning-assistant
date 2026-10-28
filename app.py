
import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI Learning Assistant", page_icon="🎓")

st.title("🎓 Multimodal AI Learning Assistant")
st.write("Ask questions using text, images, diagrams, or handwritten problems.")

question = st.text_area("Enter your question")
image = st.file_uploader(
    "Upload an image, diagram, or handwritten question",
    type=["png", "jpg", "jpeg", "webp"]
)

if st.button("Get Answer"):
    if not question.strip() and image is None:
        st.warning("Please enter a question or upload an image.")
    else:
        prompt = question or "Explain the uploaded image and solve any question shown."

        payload = {
            "model": "qwen2.5vl:3b",
            "prompt": prompt,
            "stream": False
        }

        if image is not None:
            encoded = base64.b64encode(image.getvalue()).decode("utf-8")
            payload["images"] = [encoded]

        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json=payload,
                    timeout=300
                )
                response.raise_for_status()
                answer = response.json()["response"]

            st.subheader("Answer")
            st.markdown(answer)

        except requests.RequestException:
            st.error(
                "Cannot connect to Ollama. Make sure Ollama is installed, "
                "running, and the qwen2.5vl:3b model has been downloaded."
            )

