req1 = {
    "method": "POST",
    "uri": uri("/one_chunks_mult_zero_size"),
    "version": (1, 1),
    "headers": [
        ("TRANSFER-ENCODING", "chunked")
    ],
    "body": b"",
}

req2 = {
    "method": "GET",
    "uri": uri("/second"),
    "version": (1, 1),
    "headers": [],
    "body": b""
}

req3 = {
    "method": "GET",
    "uri": uri("/third"),
    "version": (1, 1),
    "headers": [],
    "body": b""
}

request = [req1, req2, req3]
