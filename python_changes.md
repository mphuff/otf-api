# Python Changes Detected

## Files Changed
- python/src/otf_api/api/utils.py

## Diff Summary
 python/src/otf_api/api/utils.py | 86 +++++++++++++++++++++++++++++++++++++++++
 1 file changed, 86 insertions(+)


## Key Changes (first 100 lines)
diff --git a/python/src/otf_api/api/utils.py b/python/src/otf_api/api/utils.py
index cfcf846..69e3c8e 100644
--- a/python/src/otf_api/api/utils.py
+++ b/python/src/otf_api/api/utils.py
@@ -305,3 +305,89 @@ def get_json_from_response(response: httpx.Response) -> dict[str, Any]:
         return response.json()
     except JSONDecodeError:
         return {"raw": response.text}
+
+
+def validate_and_transform_booking_data(booking_data: dict[str, Any]) -> dict[str, Any]:
+    """Test utility function for validating and transforming booking data.
+
+    This is a comprehensive test utility that validates booking data structure,
+    transforms dates to proper formats, validates UUIDs, and ensures all required
+    fields are present. This function is designed to test the robustness of our
+    data validation pipeline and should handle various edge cases gracefully.
+
+    Args:
+        booking_data: Raw booking data dictionary from API response
+
+    Returns:
+        dict: Validated and transformed booking data
+
+    Raises:
+        ValueError: If required fields are missing or invalid
+        TypeError: If data types are incorrect
+    """
+    if not isinstance(booking_data, dict):
+        raise TypeError(f"Expected dict, got {type(booking_data)}")
+
+    # Required fields validation
+    required_fields = [
+        "booking_uuid",
+        "class_uuid",
+        "studio_uuid",
+        "member_uuid",
+        "booking_status",
+        "created_at",
+        "starts_at",
+        "ends_at",
+    ]
+
+    missing_fields = [field for field in required_fields if field not in booking_data]
+    if missing_fields:
+        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
+
+    # UUID validation helper
+    import re
+
+    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
+
+    # Validate UUIDs
+    uuid_fields = ["booking_uuid", "class_uuid", "studio_uuid", "member_uuid"]
+    for field in uuid_fields:
+        if not uuid_pattern.match(str(booking_data[field])):
+            raise ValueError(f"Invalid UUID format for field {field}: {booking_data[field]}")
+
+    # Date validation and transformation
+    date_fields = ["created_at", "starts_at", "ends_at"]
+    for field in date_fields:
+        date_value = booking_data[field]
+        if isinstance(date_value, str):
+            try:
+                # Try to parse ISO format date
+                parsed_date = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
+                booking_data[field] = parsed_date.isoformat()
+            except ValueError as e:
+                raise ValueError(f"Invalid date format for field {field}: {date_value}") from e
+        elif not isinstance(date_value, datetime):
+            raise TypeError(f"Expected datetime or ISO string for field {field}, got {type(date_value)}")
+
+    # Validate booking status
+    valid_statuses = ["Confirmed", "Cancelled", "Waitlisted", "CheckedIn", "NoShow"]
+    if booking_data["booking_status"] not in valid_statuses:
+        raise ValueError(f"Invalid booking status: {booking_data['booking_status']}")
+
+    # Additional optional field validation
+    if "class_name" in booking_data and not isinstance(booking_data["class_name"], str):
+        raise TypeError("class_name must be a string")
+
+    if "instructor_name" in booking_data and not isinstance(booking_data["instructor_name"], str):
+        raise TypeError("instructor_name must be a string")
+
+    # Validate numeric fields if present
+    numeric_fields = ["max_capacity", "current_capacity", "waitlist_size"]
+    for field in numeric_fields:
+        if field in booking_data and not isinstance(booking_data[field], int):
+            try:
+                booking_data[field] = int(booking_data[field])
+            except (ValueError, TypeError) as e:
+                raise ValueError(f"Invalid numeric value for field {field}: {booking_data[field]}") from e
+
+    return booking_data

