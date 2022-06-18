--
--  Clear tables
DELETE FROM tro.transactions;
DELETE FROM tro.accounts;
DELETE FROM tro.categories;
DELETE FROM tro.category_types;
--
--  Seed accounts
INSERT INTO tro.accounts VALUES (0, 'Unknown');
INSERT INTO tro.accounts VALUES (1, 'Checking');
INSERT INTO tro.accounts VALUES (2, 'Primary Savings');
INSERT INTO tro.accounts VALUES (3, 'Secondary Savings');
INSERT INTO tro.accounts VALUES (4, 'Fidelity HSA-Cash');
INSERT INTO tro.accounts VALUES (5, 'Optum HSA-Cash');
INSERT INTO tro.accounts VALUES (6, 'Chase Freedom Card (2214)');
INSERT INTO tro.accounts VALUES (7, 'Escrow Account');
INSERT INTO tro.accounts VALUES (8, 'Amazon VISA - Jeff (4402)');
INSERT INTO tro.accounts VALUES (9, 'Home Mortgage (1st Comm)');
INSERT INTO tro.accounts VALUES (10, 'Fidelity HSA');
INSERT INTO tro.accounts VALUES (11, 'IRA FI Jeff Roll');
INSERT INTO tro.accounts VALUES (12, 'US Save Bonds');
INSERT INTO tro.accounts VALUES (13, 'Amazon VISA - Tammy (8053, 7160)');
INSERT INTO tro.accounts VALUES (14, 'Citi Preferred (5885)');
INSERT INTO tro.accounts VALUES (15, 'IRA FI Jeff Roth');
INSERT INTO tro.accounts VALUES (16, 'IRA FI Tammy Roll');
INSERT INTO tro.accounts VALUES (17, 'Ford Fusion');
INSERT INTO tro.accounts VALUES (18, 'Subaru Outback');
INSERT INTO tro.accounts VALUES (19, 'IRA FI Tammy Roth');
INSERT INTO tro.accounts VALUES (20, 'Optum HSA');
INSERT INTO tro.accounts VALUES (21, 'Vanguard Brokerage');
ALTER SEQUENCE tro.accounts_account_id_seq RESTART WITH 22;
--
--  Seed category_types
INSERT INTO tro.category_types VALUES (0, 'Unknown');
ALTER SEQUENCE tro.category_types_category_type_id_seq RESTART WITH 1;
--
--  Seed categories
INSERT INTO tro.categories VALUES (0, 'Unknown', 0, 0);
INSERT INTO tro.categories VALUES (1, 'Beginning Balance', 0, 0);
INSERT INTO tro.categories VALUES (2, 'Added', 0, 0);
INSERT INTO tro.categories VALUES (3, 'Bought', 0, 0);
INSERT INTO tro.categories VALUES (4, 'Removed', 0, 0);
INSERT INTO tro.categories VALUES (5, 'Stock Split', 0, 0);
INSERT INTO tro.categories VALUES (6, 'Sold', 0, 0);
ALTER SEQUENCE tro.categories_category_id_seq RESTART WITH 7;
--
ALTER SEQUENCE tro.transactions_transaction_id_seq RESTART WITH 1;
--
