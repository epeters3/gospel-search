import React from "react";
import styled from "styled-components";

import SearchResult, { TSearchResult } from "../components/SearchResult";

const Form = styled.form`
  display: flex;
  justify-content: center;
  margin-bottom: ${(p) => p.theme.size.lg};
`;

const Input = styled.input`
  padding: ${(p) => p.theme.size.sm};
  width: 20rem;
`;

const SubmitBtn = styled.input`
  border: none;
  cursor: pointer;
`;

class Index extends React.Component {
  state: { value: string; results: TSearchResult[] };
  constructor(props) {
    super(props);
    this.state = { value: "", results: [] };
  }

  handleChange = (e) => this.setState({ value: e.target.value });

  handleSubmit = async (e) => {
    // Fetch the search results for this query.
    e.preventDefault();
    const res = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: this.state.value }),
    });
    const json = await res.json();
    console.log(json);
    this.setState({ results: json.result });
  };

  render = () => (
    <>
      <Form onSubmit={this.handleSubmit}>
        <Input
          placeholder="Search scriptures and conference talks..."
          type="text"
          value={this.state.value}
          onChange={this.handleChange}
        />
        <SubmitBtn type="submit" value="Submit" />
      </Form>
      {this.state.results.map((result) => (
        <SearchResult key={result._id} {...result} />
      ))}
    </>
  );
}

export default Index;
