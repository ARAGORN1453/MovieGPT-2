import streamlit as st 
import google.generativeai as genai
from apikey import *
from gemini_api import generation_config,safety_settings
from gemini_vision_api import generation_config_vision,safety_setting_vision
import asyncio
import shelve
from firebase_admin import credentials, auth, initialize_app,db 
import firebase_admin
cred = credentials.Certificate("moviegpt-434cd-ff02c90e02ac.json")
#default_app = firebase_admin.initialize_app(cred,{"databaseURL":"https://moviegpt-434cd-default-rtdb.firebaseio.com/"})

ref=db.reference("Users")


st.set_page_config(page_title="MovieGPT", page_icon="🎬")
st.title("MovieGPT")
st.subheader("Merhaba Ben MovieGPT. Film tavsiyesi yapan bir chatbotum.Bugün ne izlemek istersin ?")

def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages
        
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])
    
prompt = st.chat_input("Ne izlemek istersiniz.")

status_placeholder = st.empty()

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        


uploaded_file=st.file_uploader("Upload the image for movie recommendation",type=["png","jpg","jpeg"])
    

def recommend_movie(prompt,uploaded_file):
  if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    image_parts = [
      {
        "mime_type": uploaded_file.type,
        "data": file_bytes
      },
    ]
    prompt_parts_vision =  [
  "Senin adın MovieGPT.Sen film tavsiyesi yapmak için özelleşmiş bir chatbotsun.Senin görevin kullanıcıdan aldığın resmin hangi fikmden olduğunu tespit etmek ve benzer 10 filmi ekrana getirmek. Şu adımları takip etmelisin : 1.Resmin hangi filmden olduğunu tespit et ve filmin bilgilerini ekrana getir. 2.Resme göre 10 benzer film tavsiyesi yap. 3. Bu 10 filmin adını  sonra film türü,filmin özeti,filmin yönetmeni,filmin oyuncuları ve imdb puanını yazacaksın. Resimdeki film gibi onlarında bilgileri aynu şekilde yazacaksın.\n\n\n",
  image_parts[0],
  f"{prompt}",]
    response = vision_model.generate_content(prompt_parts_vision)
    return response

  else:
    prompt_parts = [
    f"input: Senin adın MovieGPT.Sen kullanıcılara film tavsiyesinde bulunmak için özelleşmiş  bir sohbet robotusun.Senin görevin kullanıcıdan  aldığın film adı,film  türü,film yönetmeni,film oyuncusu,imdb puanı parametrelerine göre benzer film tavsiyelerinde bulunmaktır.10 tane film tavsiyesi vereceksin.Önce filmin adını yazacaksın sonra film türü,filmin özeti,filmin yönetmeni,filmin oyuncuları ve imdb puanını yazacaksın.Örneğin kullanıcı {prompt} şeklinde bir prompt verdi.Bu prompta benzer 10 filmin adını,türünü,yönetmenini,oyuncularını ve imdb puanını yazıp bunları ekrana getireceksin.dinamik şekilde yanıtlar vereceksin.",
    "output: ",]
    response=text_model.generate_content(prompt_parts)
    
    return response

        
if prompt  :
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    async def generate_movie_recommendations(prompt):
        # Görsel göstergeyi güncelleyin
        status_placeholder.text("...")
        # Film önerileri üretme kodunuz burada...
        await asyncio.sleep(15)  # Uzun süren işlemi simüle edin
        response = "Generated movie recommendations"
        # Görsel göstergeyi temizleyin
        status_placeholder.empty()
        return response

    # Asenkron fonksiyonu asyncio ile çağırın
    response = asyncio.run(generate_movie_recommendations(prompt))  
    with st.chat_message("MovieGPT",avatar="🎬"):
        text_model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                )
        
        vision_model=genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config_vision,
                              )

        response=recommend_movie(prompt,uploaded_file).text
        if uploaded_file is not None:
            st.image(uploaded_file)
            
        response = recommend_movie(prompt, uploaded_file).text
        st.markdown(response )

    st.session_state.messages.append({"role": "moviegpt", "content": response}) 
         
print(st.session_state)
save_chat_history(st.session_state.messages)
ref.child("Chat History").set(st.session_state.messages)
print()















