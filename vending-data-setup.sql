INSERT INTO location (location_id, address, address_2, zip, state) VALUES
  (1, '123 Campus Dr', NULL, '84604', 'UT'),
  (2, '45 Main St', 'Suite 200', '84101', 'UT'),
  (3, '800 Tech Pkwy', NULL, '94043', 'CA');

INSERT INTO vending_machine (machine_id, location_id) VALUES
  (1, 1),
  (2, 2),
  (3, 1),
  (4, NULL);

INSERT INTO snack (name) VALUES
  ('Classic Chips'),
  ('Chocolate Bar'),
  ('Trail Mix'),
  ('Sparkling Water'),
  ('Granola Bar'),
  ('Gummy Bears');

INSERT INTO nutrition (
  snack_id, serving_size, serving_per, calories, total_fat, saturated_fat, trans_fat,
  cholesterol, sodium, total_carbohydrate, fiber, total_sugars, added_sugars, protein, additional_info
) VALUES
  (1, '1 bag (45g)', 1, 230, 14, 2, 0, 0, 180, 22, 2, 1, 0, 3, 'Potato chips; contains sunflower oil'),
  (2, '1 bar (50g)', 1, 250, 12, 7, 0, 5, 40, 29, 2, 24, 20, 3, 'Contains milk and soy'),
  (3, '1 pack (57g)', 1, 270, 16, 2, 0, 0, 90, 26, 4, 16, 10, 8, 'Contains peanuts and tree nuts'),
  (4, '1 can (355mL)', 1, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0,
