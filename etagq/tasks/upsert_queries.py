from celeryconfig import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

pg_db = {
    'drivername': 'postgres',
    'username': DB_USERNAME,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT
    }

Readers_upsert = """
INSERT INTO readers VALUES (reader_id, description, user_id)
ON CONFLICT (reader_id) DO UPDATE SET description=EXCLUDED.description, user_id=EXCLUDED.user_id;
"""

Locations_upsert = """
INSERT INTO locations VALUES (location_id, name, latitude, longitude, active)
ON CONFLICT (location_id) DO UPDATE SET name=EXCLUDED.name, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude, active=EXCLUDED.active;
"""

Animals_upsert = """
INSERT INTO animals VALUES (animal_id,species,field_data)
ON CONFLICT (animal_id) DO UPDATE SET species=EXCLUDED.species, field_data=EXCLUDED.field_data;
"""

Tags_upsert = """
INSERT INTO tags VALUES (tag_id,description)
ON CONFLICT (tag_id) DO UPDATE SET description=EXCLUDED.description;
"""

TagReads_upsert = """
INSERT INTO tag_reads VALUES (tag_reads_id,reader_id,tag_id,user_id,tag_read_time,field_data,public)
ON CONFLICT (tag_reads_id, reader_id, tag_id, tag_read_time) DO UPDATE SET reader_id=EXCLUDED.reader_id, tag_id=EXCLUDED.tag_id, tag_read_time=EXCLUDED.tag_read_time, field_data=EXCLUDED.field_data, public=EXCLUDED.public;
"""

UploadLocation_upsert = """
INSERT INTO upload_location VALUES (user_id, location_id)
ON CONFLICT (user_id, location_id) DO UPDATE SET user_id=EXCLUDED.user_id, location_id=EXCLUDED.location_id;
"""

ReaderLocation_upser = """
INSERT INTO reader_location VALUES (reader_id, location_id, start_timestamp, end_timestamp)
ON CONFLICT (reader_id) DO UPDATE SET location_id=EXCLUDED.location_id, start_timestamp=EXCLUDED.start_timestamp, end_timestamp=EXCLUDED.end_timestamp;
"""

TagOwner_upsert = """
INSERT INTO tag_owner VALUES (user_id, tag_id, start_time, end_time)
ON CONFLICT (tag_id) DO UPDATE SET user_id=EXCLUDED.user_id, start_time=EXCLUDED.start_time, end_time=EXCLUDED.end_time;
"""

AnimalHitReader_upsert = """
INSERT INTO animal_hit_reader VALUES (reader_id, animal_id, tag_id)
ON CONFLICT (reader_id, animal_id, tag_id) DO UPDATE SET reader_id=EXCLUDED.reader_id, animal_id=EXCLUDED.animal_id, tag_id=EXCLUDED.tag_id;
"""

TaggedAnimal_upsert = """
INSERT INTO tagged_animal VALUES (tag_id, animal_id, start_time, end_time, field_data)
ON CONFLICT (tag_id) DO UPDATE SET animal_id=EXCLUDED.animal_id, start_time=EXCLUDED.start_time, end_time=EXCLUDED.end_time, field_data=EXCLUDED.field_data;
"""

test_query = """select * from tags;"""
