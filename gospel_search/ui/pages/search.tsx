import React from "react";

import SearchResult, { TSearchResult } from "../components/SearchResult";
import { Form, Input, SubmitBtn } from "../components/SearchBar";

class Search extends React.Component {
  state: { value: string; results: TSearchResult[] };
  constructor(props) {
    super(props);
    this.state = { value: "", results: [] };
  }

  handleChange = (e) => this.setState({ value: e.target.value });

  handleSubmit = async (e) => {
    // Fetch the search results for this query.
    e.preventDefault();
    const res = await fetch("/api/search?" + new URLSearchParams({
      query: this.state.value,
  }).toString(), {
      method: "GET",
    });
    const json = await res.json();
    this.setState({ results: json.results });
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

export default Search;
