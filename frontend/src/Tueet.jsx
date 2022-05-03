import { Link } from "react-router-dom";

export const Tueet = (props) => {
  return (
    <div
      style={{
        marginTop: 40,
      }}
    >
      <div
        style={{
          margin: 10,
          borderRadius: 4,
          border: "2px solid",
          padding: 10,
        }}
      >
        {props.tueet.body}
      </div>
      <div
        style={{
          marginTop: 20,
        }}
      >
        {props.tueet.related_tweets.map((rt) => (
          <Link key={rt.id} to={`/tweet/${rt.id}`}>
            {rt.body}
          </Link>
        ))}
      </div>
    </div>
  );
};
