const options = {
  method: "GET",
  headers: {
    "User-Agent": "insomnia/9.2.0",
    Authorization:
      "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3OTc4ODg1LCJpYXQiOjE3Njc5NTcyODUsImp0aSI6ImNjZWEyNWNhNmVmODQ4YmViYTRjMWExNDc1NmZkNDYxIiwidXNlcl9pZCI6IjMifQ.9c1Ul9CZEF1tpS1Ne_SHEvSpjImN_8Cpz8uxC1sbvPY",
  },
};

fetch("http://127.0.0.1:8000/api/health/", options)
  .then((response) => response.json())
  .then((response) => console.log(response))
  .catch((err) => console.error(err));
