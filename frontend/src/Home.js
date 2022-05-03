import { useState, useEffect } from "react";
import { Tueet } from "./Tueet";
import { NewTweetForm } from "./NewTweetForm";
import { useParams } from "react-router-dom";

export function Home(props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [tueet, setTueet] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        setTueet(
          await (
            await fetch(`http://localhost:8000/tweet/${id ? id : "random"}/`)
          ).json()
        );
      } catch (e) {
        setError(true);
      } finally {
        setLoading(false);
      }
      console.log(tueet);
    };
    load();
  }, [id]);

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
