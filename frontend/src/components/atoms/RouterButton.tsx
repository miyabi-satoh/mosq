import { Button, ButtonProps } from "@material-ui/core";
import React from "react";
import { Link } from "react-router-dom";

type Props = ButtonProps<Link>;
export function RouterButton(props: Props) {
  return (
    <Button {...props} component={Link}>
      {props.children}
    </Button>
  );
}
