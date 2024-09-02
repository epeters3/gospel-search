import React from "react";
import { Form, Input, SubmitBtn } from "../components/SearchBar";

class QA extends React.Component {
  state: { query: string; answer: string | undefined; };
  constructor(props) {
    super(props);
    this.state = { query: "", answer: undefined };
  }

  handleChange = (e) => this.setState({ query: e.target.value });

  handleSubmit = async (e) => {
    // Fetch the search results for this query.
    e.preventDefault();
    const res = await fetch("/api/qa?" + new URLSearchParams({
      query: this.state.query,
  }).toString(), {
      method: "GET",
    });
    const json = await res.json();
    this.setState({ answer: json.answer });
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
      {this.state.answer ? <p style={{whiteSpace: 'pre-wrap'}}>{this.state.answer}</p> : null}
    </>
  );
}

export default QA;
