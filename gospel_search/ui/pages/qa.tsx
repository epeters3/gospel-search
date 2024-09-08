import React from "react";
import Markdown from "react-markdown";
import { Form, Input, SubmitBtn } from "../components/SearchBar";
import { SearchResult } from "../components/SearchResult";
import { Reference } from "../components/Reference";
import { Link } from "@mui/material";

const AgentResponse = ({
  answer,
  references,
}: {
  answer: string;
  references: SearchResult[];
}) => {
  return (
    <Markdown
      components={{
        a: ({ href, children }) => {
          if (children === "<cite>") {
            const reference = references.find((r) => r.segment.id === href);
            if (!reference) {
              console.error(`Could find no reference by ID '${href}'`);
              return undefined;
            }
            return <Reference result={reference} />;
          }
          return (
            <Link href={href} target="_blank" rel="noopener">
              {children}
            </Link>
          );
        },
      }}
    >
      {answer}
    </Markdown>
  );
};

class QA extends React.Component {
  state: {
    query: string;
    answer: string | undefined;
    references: SearchResult[];
  };
  constructor(props) {
    super(props);
    this.state = { query: "", answer: undefined, references: [] };
  }

  handleChange = (e) => this.setState({ query: e.target.value });

  handleSubmit = async (e) => {
    // Fetch the search results for this query.
    e.preventDefault();
    const res = await fetch(
      "/api/qa?" +
        new URLSearchParams({
          query: this.state.query,
        }).toString(),
      {
        method: "GET",
      }
    );
    const json = await res.json();
    this.setState({ answer: json.answer, references: json.references });
  };

  render = () => (
    <>
      <Form onSubmit={this.handleSubmit}>
        <Input
          placeholder="Ask a question..."
          type="text"
          value={this.state.query}
          onChange={this.handleChange}
        />
        <SubmitBtn type="submit" value="Submit" />
      </Form>
      {this.state.answer ? (
        <AgentResponse
          answer={this.state.answer}
          references={this.state.references}
        />
      ) : null}
    </>
  );
}

export default QA;
