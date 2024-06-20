# Các Bước ChatbotPDF cung cấp câu trả lời của người dùng dựa trên các file PDF:

- PDF Loading: Chatbot đọc nội dung của PDF và trích xuất nội dung của văn bản  
- Text Chunking: Văn bản được trích xuất được chia ra các phần nhỏ hơn để xử lý
- Language Model (API LM Studio): Chatbot dùng mô hình ngôn ngữ để tạo ra các vector biểu diễn(Embeddings) cho các đoạn văn bản vừa được chunking
- Dùng ChormaDB lưu trữ các vector của các file PDF trong ./data/ vừa được Embeddings để có một kho lưu trữ ổn định
- Có thể cập nhật lại tài liệu trong ChromaDB


#### Python==3.11
### Các bước dùng repo:
B1:
```
pip install requirements.txt
```
B2:
```
run creat_database.py
```
B3:
```
start sever trên LM Studio
```

B4:
```
streamlit run query_local_streamlit.py
```

##Sử dụng file "update_database.py" để cập nhật lại tài liệu trong DB