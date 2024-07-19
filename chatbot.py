import streamlit  as st
from langchain_community.llms import Ollama #Se importa la función
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = Ollama(model="llama3", base_url="http://localhost:11434")

#Parte I
def main():
    st.title("Chat con Llama3")
    bot_name = st.text_input("Nombre del asistente virtual:", value="Willy")
    prompt = f'eres un asistente virtual y te llamas {bot_name}, respondes preguntas con respuesta simples, además debes preguntar al usuario acorde al contexto del chat, también debes preguntarle al usuario cosas básicas para conocerlo'
    bot_description = st.text_area("Descripción del asistente virtual",
                                   value = prompt)
    
#Parte II
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    promp_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
            
        ]
    )
    
    chain = promp_template | llm
    
    user_input = st.text_input("Escribe tu pregunta:", key="user_input")
    
#Parte III
    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.stop()
            
        else: 
            response = chain.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            st.session_state["chat_history"].append(AIMessage(content=response))
#Parte IV
    chat_display= ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display+= f' 🗣️ Humano: {msg.content}\n'   
        elif isinstance(msg, AIMessage):
            chat_display += f' 🤖 {bot_name}: {msg.content}\n'
    
    
    st.text_area("Chat", value=chat_display, height=400, key="chat_area")
    
if __name__ == "__main__":
    main()
