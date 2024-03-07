import { useEffect } from "react";

export default function useAfterMount(func: () => void) {
  useEffect(() => func(), [func]);
}
