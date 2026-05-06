
for i in 10 20 30 40 50 60 70 80 90 100
do
  wrk -t4 -c${i} -d30s http://service.finik.publicvm.com/books >> logs.txt
  echo -e "\n\n" >> logs.txt
done