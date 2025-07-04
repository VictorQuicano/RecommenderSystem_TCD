import * as React from "react";
import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

type UserComboboxProps = {
  users: string[];
  selectedUser: string;
  onChange: (value: string) => void;
  label?: string;
  placeholder?: string;
};

export function UserCombobox({
  users,
  selectedUser,
  onChange,
  label = "Usuario",
  placeholder = "Selecciona un usuario",
}: UserComboboxProps) {
  const [open, setOpen] = React.useState(false);

  return (
    <div className="space-y-1">
      <label className="text-sm font-medium">{label}</label>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between font-normal"
          >
            {selectedUser || placeholder}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0">
          <Command>
            <CommandInput placeholder="Buscar usuario..." />
            <CommandEmpty>No se encontró usuario.</CommandEmpty>
            <CommandList>
              <CommandGroup>
                {users.map((user) => (
                  <CommandItem
                    key={user}
                    value={user}
                    onSelect={(currentValue) => {
                      onChange(currentValue);
                      setOpen(false);
                    }}
                  >
                    <CheckIcon
                      className={cn(
                        "mr-2 h-4 w-4",
                        selectedUser === user ? "opacity-100" : "opacity-0"
                      )}
                    />
                    {user}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
