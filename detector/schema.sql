DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS objects;

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data BLOB NOT NULL,
  label TEXT NOT NULL,
  detection_flag BOOLEAN NOT NULL 
);

CREATE TABLE objects (
  image_id INTEGER NOT NULL,
  object TEXT NOT NULL,
  FOREIGN KEY (image_id) REFERENCES images (id),
  PRIMARY KEY (image_id, object)
);
