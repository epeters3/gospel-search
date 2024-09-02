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

type BaseSegment = {
  id: string;
  parent_id: string;
  num: number;
  text: string;
  name: string;
  links: string[];
  score: number;
}

type TalkSegment = BaseSegment & {
  doc_type: "general-conference"
  talk_id: string;
  month: number;
  year: number;
}

type VerseSegment = BaseSegment & {
  doc_type: "scriptures"
}

type Segment = TalkSegment | VerseSegment

export type SearchResult = {
  segment: Segment;
}

const TalkSegmentCard = ({ parent_id, text, year, name }: TalkSegment) => (
  <Container>
    <H4>
      <a href={parent_id}>{name}
      </a>
    </H4>

    <Text>
      {text}
    </Text>
    <i>
      {`${year} Conference Talk`}
    </i>
  </Container>
)

const VerseSegmentCard = ({ parent_id, name, num, text }: VerseSegment) => (
  <Container>
    <H4>
      <a href={parent_id}>
        {`${name}:${num}`}
      </a>{" "}
    </H4>

    <Text>
      <VerseNumber> {num}</VerseNumber>
      {text}
    </Text>
    <i>
      {"Scripture"}
    </i>
  </Container>
)

export const SearchResultCard = ({ result }: { result: SearchResult }) => result.segment.doc_type === "scriptures" ? <VerseSegmentCard {...result.segment} /> : <TalkSegmentCard {...result.segment} />
