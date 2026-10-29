
import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Multimodal AI Learning Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Multimodal AI Learning Assistant")
st.write(
    "Ask questions using text, images, diagrams, "
    "or handwritten problems."
)

question = st.text_area("Enter your question")

uploaded_image = st.file_uploader(
    "Upload an image, diagram, or handwritten question",
    type=["png", "jpg", "jpeg", "webp"]
)

if st.button("Get Answer"):
    if not question.strip() and uploaded_image is None:
        st.warning("Please enter a question or upload an image.")

    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            parts = [{
                "text": question.strip()
                or "Explain the uploaded image and solve any question shown."
            }]

            if uploaded_image is not None:
                image_bytes = uploaded_image.getvalue()

                parts.append({
                    "inlineData": {
                        "mimeType": uploaded_image.type,
                        "data": base64.b64encode(
                            image_bytes
                        ).decode("utf-8")
                    }
                })

            url = (
                "https://generativelanguage.googleapis.com/"
                "v1beta/models/gemini-2.5-flash:generateContent"
            )

            response = requests.post(
                url,
                headers={
                    "x-goog-api-key": api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "contents": [{
                        "parts": parts
                    }]
                },
                timeout=120
            )

            if response.ok:
                data = response.json()
                answer = data["candidates"][0]["content"]["parts"]

                st.subheader("Answer")
                for item in answer:
                    if "text" in item:
                        st.markdown(item["text"])
            else:
                st.error(
                    f"Gemini API error ({response.status_code}): "
                    f"{response.text[:1000]}"
                )

        except KeyError:
            st.error(
                "GEMINI_API_KEY is missing from Streamlit Secrets."
            )
        except Exception as error:
            st.error(f"Something went wrong: {error}")
