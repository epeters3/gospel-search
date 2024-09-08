import { useState } from "react";
import { SearchResult, TalkSegment, VerseSegment } from "./SearchResult";
import {
  Button,
  Dialog,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Link,
} from "@mui/material";

const Verse = ({ verse }: { verse: VerseSegment }) => {
  const { parent_id, name, num, text } = verse;
  return (
    <>
      <DialogTitle>
        <Link href={parent_id} target="_blank" rel="noopener">
          {name}:{num}
        </Link>
      </DialogTitle>
      <DialogContent>
        <DialogContentText>{text}</DialogContentText>
      </DialogContent>
    </>
  );
};

const TalkParagraph = ({ paragraph }: { paragraph: TalkSegment }) => {
  const { name, text, year, month, parent_id } = paragraph;
  return (
    <>
      <DialogTitle>
        <Link href={parent_id} target="_blank" rel="noopener">
          {name}
        </Link>
      </DialogTitle>
      <DialogContent>
        <DialogContentText>{text}</DialogContentText>
        <DialogContentText style={{ fontStyle: "italic" }}>
          {month}/{year}
        </DialogContentText>
      </DialogContent>
    </>
  );
};

export const Reference = ({ result }: { result: SearchResult }) => {
  const { segment } = result;
  const [open, setOpen] = useState(false);
  return (
    <>
      <Button
        sx={{
          minWidth: 0,
          padding: 0,
          margin: 0,
          textTransform: "none",
          verticalAlign: "baseline",
        }}
        onClick={() => setOpen(true)}
      >
        ["]
      </Button>
      <Dialog onClose={() => setOpen(false)} open={open}>
        {segment.doc_type === "scriptures" ? (
          <Verse verse={segment} />
        ) : (
          <TalkParagraph paragraph={segment} />
        )}
      </Dialog>
    </>
  );
};
