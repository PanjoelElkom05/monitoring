monitoring

cara mulai
pindah directori ke monitoring 

pip install -r requirement.txt

untuk menjalankan 
python app.py


tambah instrument 
~$ curl -X POST -H 'Content-Type: application/json' localhost:5000/instrument -d '{"name": "ruang makan"}'

tambah data
~$ curl -X POST -H 'Content-Type: application/json' localhost:5000/data -d '{"temperature": 10, "humidity": 50, "instrument_id": 2}'