import AppKit
import Security

// Append this fixture to copy-keychain-password.swift in a temporary file, then
// run that file with xcrun swift -D MANAGE_SECRET_TEST on macOS.
struct ClipboardTests {
    static func run() throws {
        let account = "fixture-account"
        let service = "fixture-local-api"
        let fixture = " \tfirst\n第二行\r\n\n"
        let exactBytes = Data(("\u{FEFF}" + fixture).utf8)
        let reference = Data([1])
        let pasteboard = NSPasteboard.withUniqueName()
        defer { pasteboard.releaseGlobally() }
        let write: (Data) -> Bool = { writeClipboardText($0, to: pasteboard) }

        var requestedPassword = false
        do {
            try copyKeychainPassword(account: account, service: service, match: { query, result in
                let fields = query as NSDictionary
                if fields[kSecReturnData] as? Bool == true {
                    requestedPassword = true
                    result?.pointee = exactBytes as CFData
                } else {
                    result?.pointee = [Data([1]), Data([2])] as CFArray
                }
                return errSecSuccess
            }, write: write)
            preconditionFailure("Ambiguous selection returned success")
        } catch ClipboardCopyError.ambiguousSelection {}
        precondition(!requestedPassword, "Ambiguous selection caused a password read")
        precondition(pasteboard.data(forType: .string) == nil, "Ambiguous selection changed the clipboard")

        func matchFixture(_ payload: Data, passwordStatus: OSStatus = errSecSuccess)
            -> (CFDictionary, UnsafeMutablePointer<CFTypeRef?>?) -> OSStatus {
            return { query, result in
                let fields = query as NSDictionary
                precondition(fields[kSecClass] as? String == kSecClassGenericPassword as String)
                precondition(fields[kSecAttrAccount] as? String == account)
                precondition(fields[kSecAttrService] as? String == service)
                if fields[kSecReturnPersistentRef] as? Bool == true {
                    precondition(fields[kSecMatchLimit] as? String == kSecMatchLimitAll as String)
                    precondition(fields[kSecReturnData] == nil)
                    result?.pointee = [reference] as CFArray
                    return errSecSuccess
                }
                precondition(fields[kSecMatchItemList] as? [Data] == [reference])
                precondition(fields[kSecReturnData] as? Bool == true)
                result?.pointee = payload as CFData
                return passwordStatus
            }
        }

        try copyKeychainPassword(account: account, service: service, match: matchFixture(exactBytes), write: write)
        precondition(pasteboard.data(forType: .string) == exactBytes, "Clipboard text changed bytes")
        precondition(pasteboard.string(forType: .string) == fixture, "Clipboard text did not decode")

        do {
            try copyKeychainPassword(account: account, service: service, match: { _, result in
                result?.pointee = Data("discarded output".utf8) as CFData
                return errSecItemNotFound
            }, write: { _ in preconditionFailure("Lookup failure reached the clipboard") })
            preconditionFailure("Lookup failure returned success")
        } catch ClipboardCopyError.lookup(let status) {
            precondition(status == errSecItemNotFound)
        }

        do {
            try copyKeychainPassword(account: account, service: service,
                                     match: matchFixture(exactBytes, passwordStatus: errSecItemNotFound),
                                     write: { _ in preconditionFailure("Missing referenced item reached the clipboard") })
            preconditionFailure("Missing referenced item returned success")
        } catch ClipboardCopyError.lookup(let status) {
            precondition(status == errSecItemNotFound)
        }

        do {
            try copyKeychainPassword(account: account, service: service, match: matchFixture(Data([0xff])),
                                     write: { _ in preconditionFailure("Invalid UTF-8 reached the clipboard") })
            preconditionFailure("Invalid UTF-8 returned success")
        } catch ClipboardCopyError.invalidText {}

        do {
            try copyKeychainPassword(account: account, service: service, match: matchFixture(exactBytes), write: { _ in false })
            preconditionFailure("Clipboard write failure returned success")
        } catch ClipboardCopyError.clipboardWriteFailed {}

        print("Passed 6 clipboard checks with synthetic data and a private pasteboard.")
    }
}

try ClipboardTests.run()
