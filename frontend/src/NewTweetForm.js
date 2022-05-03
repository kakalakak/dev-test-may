import { useState } from "react";

export function NewTweetForm() {
  const [value, setValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ marginBottom: 16 }}>Tweet about anything you like!</div>
      <textarea
        style={{
          display: "block",
          width: "100%",
          borderRadius: 4,
          marginBottom: 16,
        }}
        value={value}
        onChange={(e) => setState(e.target.value)}
      />
      <button
        disabled={isLoading || !value}
        style={{ padding: "8px 16px", borderRadius: 4, alignSelf: "flex-end" }}
        onClick={() => {
          /* TODO: env for api base url */
          setIsLoading(true);
          fetch("http://localhost:8000/tweet/", {
            method: "POST",
            body: JSON.stringify({ body: value }),
            headers: {
              "Content-Type": "application/json",
            },
            /* TODO: error handling */
          })
            .then(() => {
              /* TODO: do something nicer than alert on success */
              alert("Success!");
              setValue("");
            })
            .finally(() => {
              setIsLoading(false);
            });
        }}
      >
        Create
      </button>
    </div>
  );
}
