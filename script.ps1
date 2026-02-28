curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
     -H "x-goog-api-key: AIzaSyCmH7xG-KIX0g7e2BzT_8XWKTlvmP4xmfw" \
     -H 'Content-Type: application/json' \
     -X POST \
     -d '{
           "contents": [
             {
               "parts": [
                 {
                   "text": "Explain how AI works in a single paragraph."
                 }
               ]
             }
           ]
         }'