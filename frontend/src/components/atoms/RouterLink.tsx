import { Link as MuiLink, LinkProps } from "@material-ui/core";
import { Link } from "react-router-dom";
import React, { PropsWithChildren } from "react";

type Props = LinkProps<Link>;

export function RouterLink(props: PropsWithChildren<Props>) {
  return (
    <MuiLink {...props} component={Link}>
      {props.children}
    </MuiLink>
  );
}
