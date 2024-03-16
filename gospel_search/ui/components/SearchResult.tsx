import React from "react";
import styled from "styled-components";

const Container = styled.div`
  margin-top: ${(p) => p.theme.size.xl};
`;

const H4 = styled.h4`
  margin-bottom: ${(p) => p.theme.size.xs};
`;

const Text = styled.p`
  margin: ${(p) => p.theme.size.xs} 0;
`;

const VerseNumber = styled.b`
  margin-right: ${(p) => p.theme.size.xs};
`;

export type TSearchResult = {
  _id: string;
  doc_type: string;
  name: string;
  num: string;
  parent_id: string;
  text: string;
  year: string;
};

const SearchResult = ({ doc_type, name, num, parent_id, text, year }) => (
  <Container>
    <H4>
      <a href={parent_id}>
        {doc_type == "scriptures" ? `${name}:${num}` : name}
      </a>{" "}
    </H4>

    <Text>
      {doc_type == "scriptures" ? <VerseNumber> {num}</VerseNumber> : null}
      {text}
    </Text>
    <i>
      [{doc_type === "scriptures" ? "Scripture" : `${year} Conference Talk`}]
    </i>
  </Container>
);

export default SearchResult;
