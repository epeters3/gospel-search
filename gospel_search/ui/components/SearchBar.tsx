import styled from "styled-components";

export const Form = styled.form`
  display: flex;
  justify-content: center;
  margin-bottom: ${(p) => p.theme.size.lg};
`;

export const Input = styled.input`
  padding: ${(p) => p.theme.size.sm};
  width: 20rem;
`;

export const SubmitBtn = styled.input`
  border: none;
  cursor: pointer;
`;