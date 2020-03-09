import React from "react";
import styled from "styled-components";

const Container = styled.div`
  margin-top: ${p => p.theme.size.xl};
`;

const Text = styled.p`
  margin-bottom: ${p => p.theme.size.xs};
`;

const SegmentNumber = styled.b`
  margin-right: ${p => p.theme.size.xs};
`;

const SearchResult = ({ _id, links, num, score, text }) => (
  <Container>
    <Text>
      <SegmentNumber> {num}</SegmentNumber>
      {text}
    </Text>
    <i>
      (source: <a href={_id}>{_id}</a>)
    </i>
  </Container>
);

export default SearchResult;
