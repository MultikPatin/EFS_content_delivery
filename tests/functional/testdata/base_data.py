import uuid

id_good_1 = str(uuid.uuid4())
id_good_2 = str(uuid.uuid4())
id_bad = str(uuid.uuid4())
id_invalid = "definitely not ID"
id_invalid_blank = ""

ids = [str(uuid.uuid4()) for _ in range(10)]
