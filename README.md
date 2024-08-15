Example of sending message to RabbitMQ
```bash
python sender.py send '{"id": "66b9d9e0685a198dc76f25fe", "data": {"camera_ip": "192.168.111.252", "timestamp": 1722930985, "full_img": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "crop_plate": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "license_plate": "81H57915"}}' 'LANE_VIOLATION_EXCHANGES'
```

```bash
python sender.py send '{"id": "66b9d9f9685a198dc76f25ff", "data": {"camera_ip": "192.168.111.252", "timestamp": 1722930985, "full_img": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "crop_plate": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "license_plate": "81H57915"}}' 'LINE_VIOLATION_EXCHANGES'
```

```bash
python sender.py send '{"id": "66b9021b87a7fb142d17845e", "data": {"camera_ip": "192.168.111.252", "timestamp": 1722930985, "full_img": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "crop_plate": "https://s3.oryza.vn/face/cross_line_data/test_1678.jpg", "license_plate": "HEHEHE"}}' 'WRONG_WAY_EXCHANGES'
```

Example of receiving message from RabbitMQ
```bash
python receiver.py 
```
