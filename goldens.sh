# Additional test cases to verify the improved queries
./parse -file "test_files/test.c" -use_tags_query -tags_query_dir "queries" > "goldens/test.c.golden"
./parse -file "test_files/test.cpp" -use_tags_query -tags_query_dir "queries" > "goldens/test.cpp.golden"
./parse -file "test_files/test.cs" -use_tags_query -tags_query_dir "queries" > "goldens/test.cs.golden"
./parse -file "test_files/test.dart" -use_tags_query -tags_query_dir "queries" > "goldens/test.dart.golden"
./parse -file "test_files/test.go" -use_tags_query -tags_query_dir "queries" > "goldens/test.go.golden"
./parse -file "test_files/test.java" -use_tags_query -tags_query_dir "queries" > "goldens/test.java.golden"
./parse -file "test_files/test.js" -use_tags_query -tags_query_dir "queries" > "goldens/test.js.golden"
