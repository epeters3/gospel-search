import styled from "styled-components";

export const Form = styled.form`
  display: flex;
  justify-content: stretch;
  margin-bottom: ${(p) => p.theme.size.lg};
`;

export const Input = styled.input`
  padding: ${(p) => p.theme.size.sm};
  width: 100%;
`;

export const SubmitBtn = styled.input`
  border: none;
  cursor: pointer;
`;