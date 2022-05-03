import { useState, useEffect } from "react";
import { Tueet } from "./Tueet";
import { NewTweetForm } from "./NewTweetForm";

export function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [tueet, setTueet] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        setTueet(
          await (await fetch("http://localhost:8000/tweet/random/")).json()
        );
      } catch (e) {
        setError(true);
      } finally {
        setLoading(false);
      }
      console.log(tueet);
    };
    load();
  }, []);

  if (error) {
    return <h1>oops 😅</h1>;
  }

  return !loading && tueet ? (
    <div>
      <div style={{ marginBottom: 40 }}>
        <Tueet tueet={tueet} />
      </div>
      <NewTweetForm />
    </div>
  ) : (
    <h1>Loading</h1>
  );
}
