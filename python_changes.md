# Python Changes Detected

## Files Changed
- python/src/otf_api/api/utils.py

## Diff Summary
 python/src/otf_api/api/utils.py | 64 +++++++++++++++++++++++++++++++++++++++++
 1 file changed, 64 insertions(+)


## Key Changes (first 100 lines)
diff --git a/python/src/otf_api/api/utils.py b/python/src/otf_api/api/utils.py
index cfcf846..67c55de 100644
--- a/python/src/otf_api/api/utils.py
+++ b/python/src/otf_api/api/utils.py
@@ -305,3 +305,67 @@ def get_json_from_response(response: httpx.Response) -> dict[str, Any]:
         return response.json()
     except JSONDecodeError:
         return {"raw": response.text}
+
+
+def get_json_from_response2(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response3(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response4(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response5(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response6(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response7(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response8(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}
+
+
+def get_json_from_response9(response: httpx.Response) -> dict[str, Any]:
+    """Extract JSON data from an HTTP response."""
+    try:
+        return response.json()
+    except JSONDecodeError:
+        return {"raw": response.text}

